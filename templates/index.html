<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ thống giám sát phương tiện</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f4;
            padding: 20px;
        }
        h1 {
            color: #007bff;
            margin-bottom: 10px;
        }
        #image-container {
            margin: 15px auto;
            max-width: 600px;
        }
        #vehicle-image {
            display: none;
            max-width: 100%;
            height: auto;
            border: 4px solid #007bff;
            border-radius: 10px;
        }
        #alert {
            font-size: 18px;
            color: #ff0000;
            font-weight: bold;
            display: none;
            margin-bottom: 10px;
        }
        #chart-container {
            width: 80%;
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        canvas {
            min-width: 500px;
            height: 300px !important;
        }
    </style>
</head>
<body>
    <h1>🚗 HỆ THỐNG GIÁM SÁT PHƯƠNG TIỆN 🚗</h1>

    <div id="alert">PHÁT HIỆN PHƯƠNG TIỆN!</div>

    <div id="image-container">
        <img id="vehicle-image" src="" alt="Hình ảnh phương tiện">
    </div>

    <div id="chart-container">
        <canvas id="vehicleChart"></canvas>
    </div>

    <script>
        function updateImage() {
            const img = document.getElementById('vehicle-image');
            const alertText = document.getElementById('alert');
            img.src = "/esp_feed?" + new Date().getTime();
            img.onload = function () {
                img.style.display = "block";
                alertText.style.display = "block";
            };
            img.onerror = function () {
                img.style.display = "none";
                alertText.style.display = "none";
            };
        }
        setInterval(updateImage, 2000);

        const ctx = document.getElementById('vehicleChart').getContext('2d');
        let vehicleChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        stacked: false,
                        title: { display: true, text: "Thời gian (Mỗi ảnh là 1 cụm cột)" },
                        ticks: { autoSkip: false }
                    },
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: "Số lượng phương tiện" }
                    }
                },
                plugins: {
                    legend: { position: 'top' }
                }
            }
        });

        function updateChart() {
            fetch('/get_chart_data')
                .then(response => response.json())
                .then(data => {
                    if (!data || Object.keys(data).length === 0) {
                        console.warn("⚠️ Không có dữ liệu để hiển thị.");
                        return;
                    }

                    let labels = Object.keys(data);
                    let datasets = [];
                    let vehicleTypes = new Set();

                    if (!labels.length) {
                        console.error("🚨 Dữ liệu API bị thiếu.");
                        return;
                    }

                    labels.forEach(time => {
                        if (data[time]) {
                            Object.keys(data[time]).forEach(type => vehicleTypes.add(type));
                        }
                    });

                    const colorMap = {
                        "ô tô": "#FF5733",
                        "xe máy": "#33FF57",
                        "xe tải": "#3385FF",
                        "xe buýt": "#FFD700",
                    };

                    vehicleTypes.forEach(type => {
                        let dataset = {
                            label: type,
                            data: labels.map(time => data[time][type] || 0),
                            backgroundColor: colorMap[type] || "#A9A9A9"
                        };
                        datasets.push(dataset);
                    });

                    vehicleChart.data.labels = labels;
                    vehicleChart.data.datasets = datasets;
                    vehicleChart.update();
                })
                .catch(error => console.error('🚨 Lỗi khi lấy dữ liệu:', error));
        }

        setInterval(updateChart, 5000);
        updateChart();

    </script>
</body>
</html>
