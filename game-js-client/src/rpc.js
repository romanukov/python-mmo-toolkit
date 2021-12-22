import {uuid4} from "@/utils";


export class RPC {
    constructor(serverUrl, onDisconnect) {
        this.serverUrl = serverUrl;
        this.messages = {};
        this._onDisconnect = onDisconnect;
        this._eventHandlers = {};
    }

    async connect() {
        return new Promise((resolve, reject) => {
            this.socket = new WebSocket(this.serverUrl);
            this.socket.onmessage = (e) => {
                const data = JSON.parse(e.data);
                if (data.type === 'METHOD_RESPONSE') {
                    this.messages[data.message_id] = data;
                } else if (data.type === 'EVENT') {
                    const result = data.result;
                    const eventName = result.event_name;
                    const payload = result.payload;
                    this._eventHandlers[eventName](payload);
                } else {
                    console.log(data);
                }
            }

            this.socket.onopen = e => {
                resolve(e)
            }

            this.socket.onclose = this._onDisconnect;

        })
    }

    disconnect() {
        this.socket.close();
    }

    on(eventName, func) {
        this._eventHandlers[eventName] = func;
    }

    _callMethod(methodName, args) {
        return new Promise((resolve, reject) => {
            const messageId = uuid4();
            const message = {
                message_id: messageId,
                method_name: methodName,
                data: args,
            }
            this.socket.send(JSON.stringify(message));
            const interval = setInterval(() => {
                const response = this.messages[messageId];
                if (response) {
                    if (response.success) {
                        resolve(response.result);
                    } else {
                        reject(response.result)
                    }
                    clearInterval(interval);
                    delete this.messages[messageId];
                }
            });
        });
    }

    async authorize(login, password) {
        return this._callMethod('authorize', { login, password });
    }

    async getPlayerData() {
        return this._callMethod('get_player_data', {});
    }

    async getPlayerLocation() {
        return this._callMethod('get_player_location', {});
    }

    async getLocationsAround() {
        return this._callMethod('get_locations_around', {});
    }

    async getPlayersOnLocation() {
        return this._callMethod('get_players_on_location', {});
    }

    async moveToLocation({ x, y }) {
        console.log(x, y);
        return this._callMethod('move_to_location', { x, y });
    }
}
