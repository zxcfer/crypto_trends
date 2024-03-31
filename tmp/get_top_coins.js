const CoinMarketCap = require('coinmarketcap-api');
fs = require('fs');

const apiKey = '537725aa-cba8-4015-bf66-c26be52264d1';
const client = new CoinMarketCap(apiKey);

process.argv[3]

client.getTickers().then( coins => {
	for (const x of coins['data']) {
		console.log(x);
		let filename = process.argv[2];
		fs.appendFileSync(filename, x['symbol']+',');
	}
}
).catch(console.error)
