const {Client, Collection} = require('discord.js');
const client = new Client({intents: 32767})
const { Token } = require('./config.json')

const { promisify } = require("util");
const Ascii = require("ascii-table");
const { glob } = require("glob");
const PG = promisify(glob);

client.command = new Collection()

const { Distube, default: DisTube } = require("distube");
const { SpotifyPlugin } = require("@distube/spotify");

client.distube = new DisTube(client, {
    emitNewSongOnly: true,
    leaveOnFinish: true,
    emitAddSongWhenCreatingQueue: false,
    plugins: [new SpotifyPlugin()]
})


require('./Handlers/Events')(client);
require('./Handlers/Commands')(client);

["Events", "Commands"].forEach(handler => {
    require(`.Handlers/${handler}`)(client, PG, Ascii);
});

client.login(Token);
