import asyncio
import json
import logging
from typing import Dict, Set, Any
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime, timezone

logger = logging.getLogger("intellitwin.websocket")

class EnterpriseWebSocketManager:
    def __init__(self):
        # Channel -> Set of active WebSocket instances
        self.channels: Dict[str, Set[WebSocket]] = {}
        # Client -> Subscribed channels
        self.client_channels: Dict[WebSocket, Set[str]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, initial_channel: str = "global") -> None:
        await websocket.accept()
        async with self._lock:
            if websocket not in self.client_channels:
                self.client_channels[websocket] = set()
            self.client_channels[websocket].add(initial_channel)

            if initial_channel not in self.channels:
                self.channels[initial_channel] = set()
            self.channels[initial_channel].add(websocket)

        logger.info(f"Client connected. Active clients: {len(self.client_channels)} | Initial: {initial_channel}")

    async def subscribe(self, websocket: WebSocket, channel: str) -> None:
        async with self._lock:
            if websocket in self.client_channels:
                self.client_channels[websocket].add(channel)
                if channel not in self.channels:
                    self.channels[channel] = set()
                self.channels[channel].add(websocket)

    async def unsubscribe(self, websocket: WebSocket, channel: str) -> None:
        async with self._lock:
            if channel in self.channels:
                self.channels[channel].discard(websocket)
                if not self.channels[channel]:
                    del self.channels[channel]
            if websocket in self.client_channels:
                self.client_channels[websocket].discard(channel)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            subscribed = self.client_channels.pop(websocket, set())
            for channel in subscribed:
                if channel in self.channels:
                    self.channels[channel].discard(websocket)
                    if not self.channels[channel]:
                        del self.channels[channel]
        logger.info(f"Client disconnected. Active clients: {len(self.client_channels)}")

    async def broadcast_to_channel(self, channel: str, message: Dict[str, Any]) -> None:
        if channel not in self.channels or not self.channels[channel]:
            return

        payload = json.dumps({
            "channel": channel,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": message
        })

        dead_connections: Set[WebSocket] = set()
        subscribers = list(self.channels[channel])

        async def _safe_send(ws: WebSocket):
            try:
                await ws.send_text(payload)
            except (WebSocketDisconnect, RuntimeError, ConnectionResetError):
                dead_connections.add(ws)
            except Exception as e:
                logger.error(f"Error sending frame to WebSocket client: {e}")
                dead_connections.add(ws)

        await asyncio.gather(*[_safe_send(ws) for ws in subscribers], return_exceptions=True)

        if dead_connections:
            for dead in dead_connections:
                await self.disconnect(dead)

manager = EnterpriseWebSocketManager()