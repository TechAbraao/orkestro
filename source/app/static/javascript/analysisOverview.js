$(document).ready(function () {
    const ctx = document.getElementById('mySalesPerWeek');
    const ccx = document.getElementById('myGeneralSalesStatus')
    const quantitySalesField = $(".total-sales-quantity")
    const quantityDailyRecipe = $(".total-daily-recipe")
    const btnUpdateIndicator = $(".btn-update-indicator")

    async function loadChartSalesPerWeek() {
        const res = await fetch("/api/analysis/sales-per-week");
        const dataSalesPerWeek = await res.json();

        const existing = Chart.getChart(ctx);
        if (existing) existing.destroy();

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'],
                datasets: [{
                    label: 'Pedidos',
                    data: dataSalesPerWeek.data,
                    borderWidth: 3,
                    tension: 0.5
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: 100,
                        title: {
                            display: true,
                            text: 'Quantidade de Pedidos',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            stepSize: 10,
                            callback: function (value) {
                                return value;
                            }
                        }
                    }
                }
            }
        });
    }

    async function loadGeneralSalesStatus() {
        const res = await fetch("/api/analysis/status-per-week")
        const dataGeneralSalesStatus = await res.json();

        const existing = Chart.getChart(ccx);
        if (existing) existing.destroy();

        const data = {
            labels: [
                'Cancelados',
                'Finalizados',
            ],
            datasets: [{
                label: '',
                data: dataGeneralSalesStatus.data,
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(49, 46, 129)',
                ],
                hoverOffset: 2
            }]
        };
        new Chart(ccx, {
            type: "doughnut",
            data: data
        })
    }

    async function loadTotalOrders() {
        try {
            const res = await fetch("/api/analysis/total-orders")
            const dataTotalOrders = await res.json()
            quantitySalesField.text(dataTotalOrders.data || 0)
        } catch (error) {
            window.alert(error)
        }
    }

    async function loadDailyRecipe() {
        try {
            const res = await fetch("/api/analysis/daily-recipe");
            const dataDailyRecipe = await res.json();
            quantityDailyRecipe.text(dataDailyRecipe.data || 0)
        } catch (error) {
            window.alert(error)
        }
    }

    async function refreshAll() {
        try {
            await Promise.all([
                loadChartSalesPerWeek(),
                loadGeneralSalesStatus(),
                loadTotalOrders(),
                loadDailyRecipe()
            ]);
        } catch (err) {
            window.alert(err.message);
        }
    }

    refreshAll();

    btnUpdateIndicator.on("click", refreshAll)
})