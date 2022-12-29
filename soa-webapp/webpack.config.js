const Dotenv = require('dotenv-webpack');
module.exports = {
    target: 'node',
    plugins: [
        new Dotenv()
    ],
    resolve: {
        fallback: {
            "fs": false,
            "path": false,
            "os": false
        },
    }
}