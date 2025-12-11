<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import { fly, scale } from 'svelte/transition';

  let target = 'Hello!';
  let max_generations = 500;
  let parents_mating = 10;
  let sol_per_pop = 100;
  let keep_parents = 2;
  let mutation_percent_genes = 10;

  let loading = false;
  let result = null;
  let error = null;
  let showProgress = false;
  let chartCanvas;
  let chartInstance = null;

  async function runAlgorithm() {
    loading = true;
    error = null;
    result = null;

    // Destroy existing chart
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }

    try {
      const response = await fetch('http://localhost:8000/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target,
          max_generations: Number(max_generations),
          parents_mating: Number(parents_mating),
          sol_per_pop: Number(sol_per_pop),
          keep_parents: Number(keep_parents),
          mutation_percent_genes: Number(mutation_percent_genes)
        })
      });

      const payload = await response.json().catch(() => null);

      if (!response.ok) {
        throw new Error(payload?.detail || payload?.message || 'Request failed');
      }

      result = payload;

      // Create chart after getting results
      setTimeout(() => createChart(), 80);
    } catch (err) {
      error = err?.message || String(err);
    } finally {
      loading = false;
    }
  }

  function copySolution() {
    if (!result?.final_solution) return;
    navigator.clipboard?.writeText(result.final_solution).then(() => {
      const tmp = result.copied;
      result.copied = true;
      setTimeout(() => result.copied = tmp, 1200);
    }).catch(() => {});
  }

  function createChart() {
    if (!chartCanvas || !result || !result.progress) return;

    const ctx = chartCanvas.getContext('2d');

    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: result.progress.map(p => p.generation),
        datasets: [{
          label: 'Dopasowanie',
          data: result.progress.map(p => p.fitness),
          borderColor: 'rgb(99, 102, 241)',
          backgroundColor: 'rgba(99, 102, 241, 0.12)',
          tension: 0.36,
          pointRadius: 2,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          title: {
            display: true,
            text: 'Postęp dopasowania',
            padding: { top: 6, bottom: 6 }
          },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            suggestedMax: result.max_fitness ?? undefined,
            title: { display: true, text: 'Fitness' }
          },
          x: {
            title: { display: true, text: 'Generacja' }
          }
        }
      }
    });
  }
</script>

<div class="min-h-screen bg-slate-900 text-slate-100 p-6">
  <div class="max-w-6xl mx-auto">
    <header class="mb-8 rounded-xl overflow-hidden shadow-md bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight">Algorytm Genetyczny</h1>
          <p class="mt-1 text-sm opacity-90">Ewolucja rozwiązań — od losowej populacji do dopasowanego ciągu</p>
        </div>
        <div class="text-right">
          <div class="text-xs opacity-90">Obsługiwane znaki</div>
          <div class="font-mono text-sm">ASCII + polskie znaki: ą ć ę ł ń ó ś ź ż</div>
        </div>
      </div>
    </header>

    <main class="grid lg:grid-cols-2 gap-6">
      <!-- Left: Controls -->
      <section class="rounded-xl bg-slate-800 p-6 shadow-sm" in:fly={{ y: 8 }}>
        <h2 class="text-xl font-semibold mb-4">Konfiguracja</h2>

        <div class="space-y-4">
          <label class="block">
            <div class="text-sm font-medium mb-1">Ciąg docelowy</div>
            <input type="text" bind:value={target} placeholder="Wpisz ciąg docelowy" class="w-full rounded-md border border-slate-700 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-300" />
            <div class="text-xs text-slate-300 mt-1">Tekst, który algorytm ma odgadnąć</div>
          </label>

          <label class="block">
            <div class="flex items-center justify-between">
              <div class="text-sm font-medium">Maksymalna liczba generacji</div>
              <div class="text-xs font-mono">{max_generations}</div>
            </div>
            <input type="range" min="100" max="2000" step="100" bind:value={max_generations} class="w-full mt-2" />
            <div class="flex justify-between text-xs text-slate-400 mt-1">
              <span>100</span>
              <span>1000</span>
              <span>2000</span>
            </div>
          </label>

          <div class="grid grid-cols-2 gap-3">
            <label class="block">
              <div class="text-sm font-medium mb-1">Liczba rodziców</div><div class="text-xs text-slate-400 mt-1">Ile najlepszych rozwiązań się krzyżuje</div>
              <input type="number" bind:value={parents_mating} min="1" class="w-full rounded-md border border-slate-700 px-3 py-2" />
            </label>
            <label class="block">
              <div class="text-sm font-medium mb-1">Wielkość populacji</div><div class="text-xs text-slate-400 mt-1">Liczba osobników w każdej generacji</div>
              <input type="number" bind:value={sol_per_pop} min="1" class="w-full rounded-md border border-slate-700 px-3 py-2" />
            </label>

            <label class="block">
              <div class="text-sm font-medium mb-1">Zachowane rozwiązania</div><div class="text-xs text-slate-400 mt-1">Elitaryzm - najlepsze osobniki przechodzą dalej</div>
              <input type="number" bind:value={keep_parents} min="0" class="w-full rounded-md border border-slate-700 px-3 py-2" />
            </label>
            <label class="block">
              <div class="text-sm font-medium mb-1">Wskaźnik mutacji (%)</div><div class="text-xs text-slate-400 mt-1">Procent genów podlegających losowej zmianie</div>
              <input type="number" bind:value={mutation_percent_genes} min="0" max="100" class="w-full rounded-md border border-slate-700 px-3 py-2" />
            </label>
          </div>

          <div class="flex items-center gap-3 mt-2">
            <button class="px-4 py-2 rounded-md bg-indigo-600 text-white font-semibold shadow hover:brightness-105 disabled:opacity-60" on:click={runAlgorithm} disabled={loading}>
              {#if loading}
                <svg class="inline mr-2 w-4 h-4 animate-spin" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" stroke-opacity="0.25" fill="none"></circle><path d="M22 12a10 10 0 00-10-10" stroke="currentColor" stroke-width="4" fill="none"></path></svg>
                Uruchamianie...
              {:else}
                Uruchom algorytm
              {/if}
            </button>

            <button class="px-4 py-2 rounded-md border border-slate-700 bg-slate-800" on:click={() => {
              target = '';
              max_generations = 500;
              parents_mating = 10;
              sol_per_pop = 100;
              keep_parents = 2;
              mutation_percent_genes = 10;
            }}>
              Resetuj
            </button>

          </div>
        </div>
      </section>


      <!-- Results Card -->
      <section class="rounded-xl bg-slate-800 p-6 shadow-sm" in:fly={{ y: 8, delay: 80 }}>
        <h2 class="text-xl font-semibold mb-4">Wyniki</h2>

        {#if error}
          <div class="rounded-md bg-rose-50 border border-slate-700 border border-slate-700-rose-100 p-3 mb-3">
            <div class="font-semibold text-rose-700">Błąd</div>
            <div class="text-sm text-rose-700 mt-1">{error}</div>
          </div>
        {/if}

        {#if result}
          <div class="space-y-4">
            <div class="rounded-md p-3" style="background: linear-gradient(90deg, rgba(99,102,241,0.08), rgba(79,70,229,0.04));">
              <div class="flex items-start gap-3">
                <div class="flex-1">
                  <div class="text-sm font-medium">{result.message}</div>
                  <div class="text-xs text-slate-300">Ukończono w {result.generations_completed} generacjach</div>
                </div>
                <div class="text-right">
                  <div class="text-xs text-slate-300">Dopasowanie</div>
                  <div class="font-mono text-lg">{result.fitness} / {result.max_fitness}</div>
                </div>
              </div>
            </div>

            <div class="bg-slate-800/50 border border-slate-700 rounded p-3">
              <div class="flex items-center justify-between gap-3">
                <div>
                  <div class="text-xs text-slate-300">Rozwiązanie końcowe</div>
                  <div class="font-mono break-words text-lg">{result.final_solution}</div>
                </div>
                <div class="flex flex-col items-end gap-2">
                  <button class="px-4 py-2 rounded-md bg-indigo-600 text-white font-semibold shadow hover:brightness-105 disabled:opacity-60" on:click={copySolution}>Kopiuj</button>
                  <button class="px-4 py-2 rounded-md bg-indigo-600 text-white font-semibold shadow hover:brightness-105 disabled:opacity-60" on:click={() => showProgress = !showProgress}>{showProgress ? 'Ukryj postęp' : 'Pokaż postęp'}</button>
                </div>
              </div>
              {#if result.copied}
                <div class="text-xs text-green-600 mt-2">Skopiowano do schowka</div>
              {/if}
            </div>

            <!-- Chart -->
            <div class="rounded-md border border-slate-700 p-3" style="height: 300px;">
              <canvas bind:this={chartCanvas}></canvas>
            </div>

            <!-- Progress Collapse -->
            {#if showProgress}
              <div class="mt-2 overflow-auto max-h-64 rounded border border-slate-700">
                <table class="w-full text-sm">
                  <thead class="bg-black-100 sticky top-0">
                    <tr class="text-left">
                      <th class="px-3 py-2">Gen</th>
                      <th class="px-3 py-2">Rozwiązanie</th>
                      <th class="px-3 py-2">Dopasowanie</th>
                    </tr>
                  </thead>
                  <tbody>
                    {#each result.progress as item (item.generation)}
                      <tr class="border border-slate-700-t hover:bg-slate-800/50">
                        <td class="px-3 py-2 font-mono">{item.generation}</td>
                        <td class="px-3 py-2 font-mono break-words">{item.solution}</td>
                        <td class="px-3 py-2">{item.fitness}/{item.max_fitness}</td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
              </div>
            {/if}
          </div>

        {:else if !loading}
          <div class="flex flex-col items-center justify-center py-12 opacity-60">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <p class="text-sm">Uruchom algorytm, aby zobaczyć wyniki</p>
          </div>
        {/if}

        {#if loading}
          <div class="mt-4 flex items-center gap-3">
            <div class="animate-pulse w-9/12 h-8 rounded bg-slate-100"></div>
            <div class="text-sm text-slate-300">Ewolucja rozwiązań w toku...</div>
          </div>
        {/if}
      </section>
    </main>

    <footer class="mt-6 text-center text-xs text-slate-300">Mały interfejs do eksperymentów z parametrami: zmieniaj mutacje, elitaryzm i populację.</footer>
  </div>
</div>

<style>
  /* Minimal global reset for this component */
  :global(body) { margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }
</style>
