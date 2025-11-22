<script>
    let canvas;
    let ctx;
    let isDrawing = false;
    let prediction = null;
    let loading = false;
    let error = null;

    const API_URL = 'http://127.0.0.1:8000'
    function initCanvas(node) {
        ctx = canvas.getContext('2d');
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, 350, 350);
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 20;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
    }

    function startDrawing(e) {
        isDrawing = true;
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    function draw(e) {
        if (!isDrawing) return;
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        ctx.lineTo(x, y);
        ctx.stroke();
    }

    function stopDrawing() {
        isDrawing = false;
    }

    function clearCanvas() {
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, 350, 350);
        prediction = null;
        error = null;
    }

    async function recognize() {
        loading = true;
        error = null;
        prediction = null;

        try {
            const blob = await new Promise(resolve => canvas.toBlob(resolve));
            const formData = new FormData();
            formData.append('file', blob, 'drawing.png');
            const response = await  fetch(`${API_URL}/predict`, {
                method: 'POST',
                body: formData
            });

            const data = await  response.json();

            if (data.success) {
                prediction = data;
            } else {
                error = data.error || 'Recognition failed';
            }
        } catch (error) {
            error ='Error: ' + error.message;
        } finally {
            loading = false;
        }
    }
</script>

<div class="min-h-screen bg-gradient-to-br 
    from-[#780b12]/60 
    via-[#000000]/50
    via-[#000000] 
    via-[#4a0003]/10
    to-[#780b12]/30 
    flex items-center justify-center p-6">
    <div class="backdrop-blur-xl bg-white/5 border-2 border-[#fbff00] shadow-[0_0_30px_#fbff00] rounded-2xl w-full max-w-4xl p-10">

        
        <h2 class="text-4xl font-bold text-center text-white mb-2">
            🔢 MNIST Digit Recognizer
        </h2>
        <p class="text-center text-gray-300 mb-8">
            Narysuj cyfrę 0–9, a AI spróbuje ją odgadnąć.
        </p>

        <div class="flex justify-center mb-8">
            <canvas
                bind:this={canvas}
                use:initCanvas
                width="350"
                height="350"
                class="border-4 border-[#fbff00] shadow-[0_0_20px_#fbff00] bg-black rounded-xl cursor-crosshair"
                on:mousedown={startDrawing}
                on:mousemove={draw}
                on:mouseup={stopDrawing}
                on:mouseleave={stopDrawing}
            />
        </div>

        <div class="flex gap-4 justify-center mb-8">
            <button
                class="px-6 py-3 rounded-lg bg-[#fbff00] text-black font-semibold shadow-[0_0_15px_#fbff00] hover:bg-[#ffff66] transition"
                disabled={loading}
                on:click={recognize}
            >
                {#if loading}
                    ⏳ Rozpoznawanie...
                {:else}
                    Rozpoznaj
                {/if}
            </button>

            <button
                class="px-6 py-3 rounded-lg bg-[#fbff00]/10 text-gray-200 font-semibold hover:bg-[#fbff00]/20 transition border border-[#fbff00]/20"
                on:click={clearCanvas}
            >
                Wyczyść
            </button>
        </div>

        {#if error}
            <div class="text-red-400 text-center font-semibold mb-6">
                ⚠️ {error}
            </div>
        {/if}

        {#if prediction}
            <div class="bg-white/5 border border-white/10 rounded-xl p-6 mb-6">
                <div class="text-center">
                    <div class="text-7xl font-bold text-[#00e5ff] drop-shadow-[0_0_20px_#00e5ff] mb-4">
                        {prediction.predicted_digit}
                    </div>
                    <div class="text-gray-300">
                        {(prediction.confidence * 100).toFixed(1)}% pewności
                    </div>
                </div>

                <div class="mt-6 text-gray-300 space-y-3">
                    {#each Object.entries(prediction.probabilities) as [digit, prob]}
                        <div class="flex items-center gap-3">
                            <span class="w-8 font-bold text-white">{digit}</span>
                            <progress
                                class="progress w-full"
                                value={prob * 100}
                                max="100"
                            ></progress>
                            <span class="w-16 text-right opacity-70">
                                {(prob * 100).toFixed(1)}%
                            </span>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    </div>
</div>


<style>
    :global(body) {
        background-color: #0f0f1a;
        color: white;
        margin: 0;
        font-family: 'Inter', sans-serif;
    }

    progress::-webkit-progress-value {
        background: #ff0000;
    }
    progress::-webkit-progress-bar {
        background: rgba(255, 255, 255, 0.1);
    }

</style>

