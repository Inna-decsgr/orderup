<template>
  <div style="margin-top: 20px;">
    <h6 style="text-align: center;"><strong>최근 가장 많이 주문된 메뉴</strong></h6>
    <div>
      <canvas id="myChart"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart, DoughnutController, ArcElement, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import axios from 'axios';

Chart.register(DoughnutController, ArcElement, Tooltip, Legend, ChartDataLabels);

export default {
  data() {
    return {
      chartData: {
        labels: [],
        data: []
      }
    }
  },
  methods: {
    async getChartData() {
      try {
        const response = await axios.get('https://orderup-7zpo6e91n-innas-projects-81fd8c82.vercel.app/order/popular_menu/');
        this.chartData = response.data;
        console.log(this.chartData);
        this.createChart();
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    },
    createChart() {
      const ctx = document.getElementById('myChart').getContext('2d');
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: this.chartData.labels,
          datasets: [{
            data: this.chartData.data,
            backgroundColor: [
              '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6B6B', '#C9CBCF'
            ]
          }]
        },
        options: {
          plugins: {
            tooltip: {
              callbacks: {
                label: function (tooltipItem) {
                  return tooltipItem.label + ': ' + tooltipItem.raw; // 툴팁에서 숫자도 보이게
                }
              }
            },
            datalabels: {
              color: 'white',
              font: {
                weight: 'bold'
              },
              formatter: (value) => {
                // 메뉴명과 주문량을 함께 표시
                //const label = ctx.chart.data.labels[ctx.dataIndex];
                return value;
              },
              anchor: 'center',
              align: 'center',
            }
          }
        }
      });
    }
  },
  mounted() {
    this.getChartData();
  }
};
</script>


<style>
canvas {
  max-width: 800px;
  margin: 10px auto;
}
</style>