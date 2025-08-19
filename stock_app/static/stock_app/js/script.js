<script>
let typingTimer;
const typingDelay = 800; // milliseconds after typing stops

function fetchStock() {
    const symbol = document.getElementById('symbol').value.trim();
    if (!symbol) return;

    fetch(`/get_stock_data/?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            if (data.price) {
                document.getElementById('stockPrice').innerText =
                    `${data.symbol}: $${data.price}`;
            } else {
                document.getElementById('stockPrice').innerText =
                    `Error: ${data.error}`;
            }
        })
        .catch(() => {
            document.getElementById('stockPrice').innerText = 'Error fetching data';
        });
}

// Trigger fetch after user stops typing
document.getElementById('symbol').addEventListener('input', () => {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(fetchStock, typingDelay);
});

// Auto-refresh every 10 seconds
setInterval(fetchStock, 10000);

// Initial load
fetchStock();
</script>
