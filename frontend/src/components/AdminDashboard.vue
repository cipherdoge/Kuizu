<template>
  <div class="dashboard">
    <h1>Admin Dashboard</h1>
    <router-link to="/manage-quiz" class="manage-quiz-btn">Manage Quizzes</router-link>
    <!-- Statistics Cards -->
    <div class="statistics-grid">
      <div class="stat-card">
        <h3>Total Users</h3>
        <div class="stat-value">{{ statistics.total_users }}</div>
      </div>
      <div class="stat-card">
        <h3>Total Subjects</h3>
        <div class="stat-value">{{ statistics.total_subjects }}</div>
      </div>
      <div class="stat-card">
        <h3>Total Quizzes</h3>
        <div class="stat-value">{{ statistics.total_quizzes }}</div>
      </div>
    </div>

    <!-- Recent Scores Table -->
    <div class="recent-scores">
      <h2>Recent Quiz Attempts</h2>
      <table>
        <thead>
          <tr>
            <th>User</th>
            <th>Quiz ID</th>
            <th>Score</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="score in recentScores" :key="score.quiz_id + score.timestamp">
            <td>{{ score.user }}</td>
            <td>{{ score.quiz_id }}</td>
            <td>{{ score.score.toFixed(1) }}%</td>
            <td>{{ formatDate(score.timestamp) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      statistics: {
        total_users: 0,
        total_subjects: 0,
        total_quizzes: 0
      },
      recentScores: []
    }
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await axios.get('/api/admin/dashboard/summary', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.statistics = response.data.statistics;
        this.recentScores = response.data.recent_scores;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    },
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleString();
    }
  },
  mounted() {
    this.fetchDashboardData();
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-value {
  font-size: 2em;
  font-weight: bold;
  color: #2c3e50;
}

.recent-scores {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
}
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.manage-quiz-btn {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s;
}

.manage-quiz-btn:hover {
  background-color: #45a049;
}
</style>
