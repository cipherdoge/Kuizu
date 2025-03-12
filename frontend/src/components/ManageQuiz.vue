<template>
  <div class="manage-quiz-container">
    <h1>Manage Quizzes</h1>

    <!-- Search Section -->
    <div class="search-section">
      <input
        v-model="searchQuery"
        placeholder="Search users, subjects, or quizzes..."
        class="search-input"
      />
      <select v-model="searchType" class="search-select">
        <option value="users">Users</option>
        <option value="subjects">Subjects</option>
        <option value="quizzes">Quizzes</option>
      </select>
      <button @click="search" type="button" class="btn btn-primary">Search</button>
    </div>

    <!-- Search Results -->
    <div v-if="searchPerformed">
      <h2 v-if="searchResults.length">Search Results</h2>
      <p v-else>No results found for your query.</p>
      <div class="results-list">
        <template v-if="searchType === 'quizzes'">
          <div v-for="(result, index) in searchResults" :key="result.id" class="result-item">
            <p><strong>ID:</strong> {{ result.id }}</p>
            <p><strong>Remarks:</strong> 
              <span v-if="!result.editing">{{ result.remarks }}</span>
              <input v-else v-model="result.remarks" />
            </p>
            <p><strong>Chapter ID:</strong> 
              <span v-if="!result.editing">{{ result.chapter_id }}</span>
              <input v-else v-model="result.chapter_id" />
            </p>
            <button v-if="!result.editing" @click="enableEdit(index)" class="btn btn-warning">Edit</button>
            <button v-if="result.editing" @click="saveEdit(index, result)" class="btn btn-success">Save</button>
            <button v-if="result.editing" @click="cancelEdit(index)" class="btn btn-secondary">Cancel</button>
            <button @click="deleteQuiz(result.id)" class="btn btn-danger">Delete</button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      searchQuery: "",
      searchType: "subjects",
      searchResults: [],
      searchPerformed: false,
    };
  },
  methods: {
    async search() {
      if (!this.searchQuery.trim()) {
        alert("Please enter a search query.");
        return;
      }

      const token = localStorage.getItem("token");
      if (!token) {
        alert("Authentication token missing. Please log in.");
        return;
      }

      try {
        const response = await axios.get("/api/admin/search", {
          params: {
            query: this.searchQuery,
            type: this.searchType,
          },
          headers: { Authorization: `Bearer ${token}` },
        });

        this.searchResults = response.data.map(quiz => ({
          ...quiz,
          editing: false, // Add an `editing` field to each quiz item
        }));
        this.searchPerformed = true;
      } catch (error) {
        console.error("Error during search:", error);
        this.handleError(error);
      }
    },
    
    enableEdit(index) {
      this.searchResults[index].editing = true;
    },

    async saveEdit(index, result) {
      try {
        const token = localStorage.getItem("token");
        await axios.put(`/api/admin/updatequiz/${result.id}`, {
          remarks: result.remarks,
          chapter_id: result.chapter_id,
        }, {
          headers: { Authorization: `Bearer ${token}` },
        });

        this.searchResults[index].editing = false;
      } catch (error) {
        console.error("Error updating quiz:", error);
        this.handleError(error);
      }
    },

    cancelEdit(index) {
      this.searchResults[index].editing = false;
      this.search(); // Refresh data from API to restore original values
    },

    async deleteQuiz(quizId) {
      if (!confirm("Are you sure you want to delete this quiz?")) return;

      try {
        const token = localStorage.getItem("token");
        await axios.delete(`/api/admin/deletequiz/${quizId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        this.searchResults = this.searchResults.filter(quiz => quiz.id !== quizId);
      } catch (error) {
        console.error("Error deleting quiz:", error);
        this.handleError(error);
      }
    },

    handleError(error) {
      if (error.response?.status === 401) {
        alert("Unauthorized access. Please log in again.");
      } else if (error.response?.status === 403) {
        alert("Admin access required.");
      } else if (error.response?.status === 422) {
        alert("Invalid search query or parameters.");
      } else {
        alert("An error occurred. Please try again.");
      }
    },
  },
};
</script>

<style>
.manage-quiz-container {
  padding: 20px;
}

.search-section {
  margin-bottom: 20px;
}

.search-input {
  padding: 5px;
  margin-right: 10px;
}

.search-select {
  margin-right: 10px;
}

.results-list {
  margin-top: 20px;
}

.result-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
}

.btn {
  margin-right: 5px;
}
</style>
