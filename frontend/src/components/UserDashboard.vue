<template>
  <div class="user-dashboard">
    <h1>User Dashboard</h1>
    
    <!-- Displaying User Statistics -->
    <div v-if="userStats">
      <h2>Statistics</h2>
      <p>Total Attempts: {{ userStats.total_attempts }}</p>
      <p>Average Score: {{ userStats.average_score.toFixed(2) }}%</p>

      <!-- Adding a Bar Chart for Statistics -->
      <div class="chart-container">
        <BarChart :data="statisticsChartData" />
      </div>

      <!-- Displaying Recent Attempts -->
      <h3>Recent Attempts</h3>
      <ul v-if="userStats.recent_attempts.length">
        <li v-for="attempt in userStats.recent_attempts" :key="attempt.quiz_id">
          <strong>{{ attempt.chapter_name }}:</strong> Score: {{ attempt.score }}% 
          <br>
          Date: {{ attempt.attempt_date }}
        </li>
      </ul>
      <p v-else>No recent attempts</p>

      <!-- Adding a Line Chart for Recent Attempts Scores -->
      <div class="chart-container">
        <LineChart :data="recentAttemptsChartData" />
      </div>
    </div>
    
    <!-- Error or Loading State -->
    <div v-else>
      <p v-if="loading">Loading...</p>
      <p v-else-if="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { defineComponent } from 'vue';
import { Bar,Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, Title, Tooltip, Legend, BarElement, PointElement } from 'chart.js';

// Register necessary Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,PointElement);


export default defineComponent({
  name: 'UserDashboard',
  components: {
    BarChart: Bar,
    LineChart: Line
  },
  setup() {
    const userStats = ref(null);
    const loading = ref(true);
    const error = ref('');

    const statisticsChartData = ref({
      labels: ['Total Attempts', 'Average Score'],
      datasets: [{
        label: 'User Stats',
        data: [0, 0], // Default data, will be updated after fetching
        backgroundColor: ['#42A5F5', '#66BB6A'],
        borderColor: ['#42A5F5', '#66BB6A'],
        borderWidth: 1
      }]
    });

    const recentAttemptsChartData = ref({
      labels: [], // Quiz dates will be added here
      datasets: [{
        label: 'Scores of Recent Attempts',
        data: [], // Scores will be added here
        fill: false,
        borderColor: '#FF5733',
        tension: 0.1
      }]
    });

    // Fetch user dashboard data
    const fetchUserDashboard = async () => {
      console.log('Fetching user dashboard...');
      const token = localStorage.getItem('token');

      if (!token) {
        error.value = 'No token found. Please log in again.';
        loading.value = false;
        return;
      }

      try {
        const response = await axios.get('/api/user/dashboard/summary', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log('Response:', response);

        userStats.value = {
          ...response.data.statistics,
          recent_attempts: response.data.recent_attempts
        };

        // Update the statistics chart data
        statisticsChartData.value.datasets[0].data = [
          userStats.value.total_attempts,
          userStats.value.average_score
        ];

        // Update the recent attempts chart data
        recentAttemptsChartData.value.labels = userStats.value.recent_attempts.map(attempt => attempt.attempt_date);
        recentAttemptsChartData.value.datasets[0].data = userStats.value.recent_attempts.map(attempt => attempt.score);

        loading.value = false;
      } catch (err) {
        error.value = 'Failed to load user dashboard data. Please try again later.';
        loading.value = false;
      }
    };

    // Call fetchUserDashboard when the component is mounted
    onMounted(fetchUserDashboard);

    return { userStats, loading, error, statisticsChartData, recentAttemptsChartData };
  },
});
</script>

<style scoped>
.user-dashboard {
  padding: 20px;
  max-width: 800px;
  margin: auto;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

h2, h3 {
  margin-top: 20px;
  font-size: 1.5em;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  margin-bottom: 10px;
}

.chart-container {
  margin-top: 20px;
  height: 300px;
}
</style>
