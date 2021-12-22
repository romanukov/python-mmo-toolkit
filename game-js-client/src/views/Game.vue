<template>
    <div class="game">
        <div class="login-window" v-if="!token">
            <div class="error-message" v-if="errorMessage">
                {{ errorMessage }}
            </div>

            <div class="login-window__row">
                <label for="login">Login</label>
                <input type="text" id="login" v-model="login" />
            </div>
            <div class="login-window__row">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="password" />
            </div>
            <div class="login-window__row">
                <button @click="authorize">Authorize</button>
            </div>
            <div class="login-window__row" v-if="token">
                <button @click="getPlayerData">Get player data</button>
            </div>
            <div class="login-window__row" v-if="token">
                <button @click="getPlayerLocation">Get player location</button>
            </div>
            <div class="login-window__row" v-if="token">
                <button @click="getLocationsAround">Get locations around</button>
            </div>
            <div class="login-window__row" v-if="token">
                <button @click="getPlayersOnLocation">Get players on location</button>
            </div>
        </div>

        <div class="game__content" v-if="token">

            <div :class="locationCssClass" v-if="currentLocation">

                <div class="mini-map" v-if="miniMap">
                    <div class="mini-map__row" v-for="row in miniMap">
                        <div :class="miniMapCellCssClass(cell)" v-for="cell in row" @click="moveToLocation(cell)"></div>
                    </div>
                    <div class="location__name">{{ currentLocation.name }} [{{ currentLocation.x }}, {{ currentLocation.y }}]</div>
                </div>
            </div>

            <ul class="player-info">
                {{ playerData }}
            </ul>

            <div class="inventory__equip">
                <div class="inventory__equip">
                    <div class="inventory__equip-cell">Head</div>
                    <div class="inventory__equip-cell">Body</div>
                    <div class="inventory__equip-cell">LA</div>
                    <div class="inventory__equip-cell">RA</div>
                    <div class="inventory__equip-cell">Legs</div>
                    <div class="inventory__equip-cell">Feet</div>
                    <div class="inventory__equip-cell">LW</div>
                    <div class="inventory__equip-cell">RW</div>
                </div>

                <div class="inventory__items">
                    <ul>
                        <li>
                            Helmet
                            <button>Equip</button>
                            <button>Close</button>
                        </li>
                        <li>
                            Jacket
                            <button>Equip</button>
                            <button>Close</button>
                        </li>
                        <li>
                            Trousers
                            <button>Equip</button>
                            <button>Close</button>
                        </li>
                        <li>
                            Boots
                            <button>Equip</button>
                            <button>Close</button>
                        </li>
                        <li>
                            Supressor
                            <button>Equip</button>
                            <button>Close</button>
                        </li>
                    </ul>
                </div>
            </div>

            <ul class="location-info">
                {{ currentLocation }}
            </ul>

            <ul class="players-on-location">
                <li v-for="player in playersOnLocation">
                    <span :class="player.online ? '--online' : '--offline'">{{ player.name }} [1]</span>
                </li>
            </ul>

            <button @click="logout">Logout</button>
        </div>
    </div>
</template>

<script>
import {uuid4} from "@/utils";
import {RPC} from "@/rpc";

const errorMessages = {
    'BAD_CREDENTIALS': 'Bad credentials',
}

export default {
    name: 'Game',
    data: () => ({
        /** @type {RPC} */rpc: null,
        login: '',
        password: '',
        errorMessage: null,
        token: null,
        miniMap: null,
        currentLocation: null,
        playerData: null,
        /** @type {Array} */playersOnLocation: null,
    }),
    computed: {
        locationCssClass() {
            const classes = {
                'location': true,
            };
            const groundType = this.currentLocation.ground_type;
            classes['--' + groundType.toLowerCase()] = true;
            return classes;
        },
    },
    methods: {
        miniMapCellCssClass(cell) {
            const classes = {
                'mini-map__cell': true,
            };
            if (cell) {
                if (cell.x === this.currentLocation.x && cell.y === this.currentLocation.y) {
                    classes['--current'] = true;
                }
                const groundType = cell.ground_type;
                classes['--' + groundType.toLowerCase()] = true;
            }
            return classes;
        },

        initializeEvents() {
            this.rpc.on('player_data_changed', payload => {
                for (const locationPlayer of this.playersOnLocation) {
                    if (locationPlayer.id === payload.id) {
                        locationPlayer.online = payload.online;
                        console.log(locationPlayer);
                    }
                }
            });
            this.rpc.on('player_leave_on_location', payload => {
                const index = this.playersOnLocation.findIndex(v => v.id === payload.id);
                this.playersOnLocation.splice(index, 1);
            });
            this.rpc.on('player_entered_on_location', payload => {
                this.playersOnLocation.push(payload);
            });
        },

        async authorize() {
            this.rpc = new RPC("ws://localhost:3000", () => {
                this.token = null;
            });
            await this.rpc.connect();
            try {
                const result = await this.rpc.authorize(this.login, this.password);
                this.errorMessage = '';
                console.log('result', result.token);
                this.token = result.token;

                await this.getPlayerData();
                await this.getPlayerLocation();
                await this.getLocationsAround();
                await this.getPlayersOnLocation();
                this.initializeEvents();
            } catch (e) {
                console.log('err', e);
                this.errorMessage = errorMessages[e.code];
                this.rpc.disconnect();
            }
        },
        async logout() {
            await this.rpc.disconnect();
            this.token = null;
            this.miniMap = null;
            this.playersOnLocation = null;
        },
        async getPlayerData() {
            try {
                this.playerData = await this.rpc.getPlayerData();
            } catch (e) {
                console.log('err', e);
            }
        },
        async getPlayerLocation() {
            try {
                this.currentLocation = await this.rpc.getPlayerLocation();
            } catch (e) {
                console.log('err', e);
            }
        },
        async getLocationsAround() {
            try {
                this.miniMap = await this.rpc.getLocationsAround();
                console.log('result', this.miniMap);
            } catch (e) {
                console.log('err', e);
            }
        },
        async getPlayersOnLocation() {
            try {
                this.playersOnLocation = await this.rpc.getPlayersOnLocation();
                console.log('result', this.playersOnLocation);
            } catch (e) {
                console.log('err', e);
            }
        },
        async moveToLocation(cell) {
            if (!cell) return;

            try {
                await this.rpc.moveToLocation({ x: cell.x, y: cell.y });
                await this.getLocationsAround();
                await this.getPlayerLocation();
                await this.getPlayersOnLocation();
            } catch (e) {
                console.log('err', e);
            }
        },
    },
}
</script>

<style lang="stylus">

$grass-color = #054e05
$grass-color-hover = #0A680A

$soil-color = #5e1f0d
$soil-color-hover = #612a19

$water-color = #32bac7
$water-color-hover = #37d1e0

.error-message
    padding 16px
    border 1px solid darkred
    background indianred
    color white
    margin-bottom 16px

.mini-map
    display flex
    flex-direction column
    position absolute
    top 0
    right 0
    padding 8px
    background #eee

    &__row
        display flex
        flex-direction row
        margin-bottom 1px

    &__cell
        width 32px
        height 16px
        border 1px solid #333
        background #333
        margin-left 1px

        &.--current
            opacity 0.5
            cursor default !important

        &.--grass
            background $grass-color
            cursor pointer

            &:hover
                background $grass-color-hover

        &.--soil
            background $soil-color
            cursor pointer

            &:hover
                background $soil-color-hover

        &.--water
            background $water-color
            cursor pointer

            &:hover
                background $water-color-hover

.players-on-location
    li
        list-style none
        cursor pointer

        span
            font-weight bold

            &.--online
                color #111

                &:hover
                    color #555

            &.--offline
                color #999


.location
    width 512px
    height 256px
    margin auto
    position relative

    &.--grass
        background $grass-color

    &.--soil
        background $soil-color

    &.--water
        background $water-color

.inventory
    &__equip
        display flex

    &__equip-cell
        width 48px
        height 48px
        border 1px solid #333

        &.--head
            pass

        &.--body
            pass

        &.--left-arm
            pass

        &.--right-arm
            pass

        &.--legs
            pass

        &.--feet
            pass



</style>
