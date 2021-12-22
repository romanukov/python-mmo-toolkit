<template>
    <div class="locations-editor">
        <div>
            <label>
                Location width:
                <input type="number" v-model.number="locationWidth" />
            </label>
            <label>
                Location height:
                <input type="number" v-model.number="locationHeight" />
            </label>
        </div>

        <div class="row">
            <table>
                <tbody>
                    <tr v-for="row in cells">
                        <td v-for="cell in row"
                            :class="`location-cell --${cell.type.toLowerCase()} ${activeCellClass(cell)}`"
                            @click="selectCell(cell)">
                            <span v-if="cell.blocked">X</span>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div class="cell-info" v-if="currentCell">
                <h2>Cell [{{ currentCell.x }}, {{ currentCell.y }}]</h2>
                <div class="row">
                    Type:
                    <select v-model="currentCell.type">
                        <option value="NONE">None</option>
                        <option value="SOIL">Soil</option>
                        <option value="GRASS">Grass</option>
                        <option value="WATER">Water</option>
                    </select>
                </div>
                <div class="row">
                    Blocked:
                    <input type="checkbox" v-model="currentCell.blocked">
                </div>
                <button>Save</button>
            </div>

        </div>
    </div>
</template>

<script>

const CELL_TYPES = {
    NONE: 'NONE',
    SOIL: 'SOIL',
    GRASS: 'GRASS',
    WATER: 'WATER',
}

export default {
    name: 'LocationsEditor',
    data: () => ({
        locationWidth: 5,
        locationHeight: 5,
        currentCell: null,
        cells: [],
    }),
    methods: {
        generateCells(/** @type{Array<object>} */cells, width, height) {
            const resultCells = [];
            for (let y = 0; y < height; ++y) {
                resultCells[y] = [];
                for (let x = 0; x < width; ++x) {
                    resultCells[y][x] = {
                        x, y,
                        type: CELL_TYPES.SOIL,
                        blocked: false,
                    }
                }
            }

            for (const cell in cells) {
                const resultCell = resultCells[cell.y][cell.x];
                resultCell.type = cell.type;
                resultCell.blocked = cell.blocked;
            }

            return resultCells;
        },

        loadLocationMap(id) {
            const locationCells = [];
            const width = 10;
            const height = 10;

            this.cells = this.generateCells(locationCells, width, height);
        },

        activeCellClass(cell) {
            if (cell === this.currentCell) {
                return '--active';
            }
            return '';
        },

        selectCell(cell) {
            this.currentCell = cell;
        },
    },
    created() {
        this.loadLocationMap();
    },
    components: {
    }
}
</script>

<style lang="stylus">

.row
    display flex

.cell-info
    padding 16px 32px
    border 1px dashed #333
    margin-left 16px

.location-cell
    width 32px
    height 32px
    cursor pointer
    color white
    border 1px solid transparent
    font-weight bold

    &.--active
        border-color red

    &.--none
        background #000

        &:hover
            background #111

    &.--water
        background #5188e8

        &:hover
            background #4168F8

    &.--soil
        background #452525

        &:hover
            background #654545

    &.--grass
        background #008000

        &:hover
            background #109010

</style>
