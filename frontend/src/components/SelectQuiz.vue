<template>
  <div class="quiz-selector">
    <h2>Select a Quiz</h2>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else class="selector-container">
      <!-- Subject Selection -->
      <div class="select-group">
        <label for="subject">Select Subject:</label>
        <select v-model="selectedSubject" @change="loadChapters" id="subject">
          <option value="">Choose a subject</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
            {{ subject.name }}
          </option>
        </select>
      </div>

      <!-- Chapter Selection -->
      <div class="select-group">
        <label for="chapter">Select Chapter:</label>
        <select v-model="selectedChapter" @change="loadQuizzes" id="chapter" :disabled="!selectedSubject">
          <option value="">Choose a chapter</option>
          <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
            {{ chapter.name }}
          </option>
        </select>
      </div>

      <!-- Quiz Selection -->
      <div class="select-group">
        <label for="quiz">Select Quiz:</label>
        <select v-model="selectedQuiz" id="quiz" :disabled="!selectedChapter">
          <option value="">Choose a quiz</option>
          <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
            Quiz {{ quiz.id }} - {{ formatDate(quiz.date_of_quiz) }} ({{ formatDuration(quiz.time_duration) }})
          </option>
        </select>
      </div>
    </div>

    <button 
      :disabled="!selectedQuiz" 
      class="take-quiz-btn"
      @click="handleQuizStart"
    >
      Take Quiz
    </button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'UserHome',
  setup() {
    const router = useRouter()
    const subjects = ref([])
    const chapters = ref([])
    const quizzes = ref([])
    const selectedSubject = ref('')
    const selectedChapter = ref('')
    const selectedQuiz = ref('')
    const loading = ref(false) // Loading state

    const loadSubjects = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/subjects')
        subjects.value = response.data
      } catch (error) {
        console.error('Error loading subjects:', error)
        alert('Failed to load subjects. Please try again later.')
      } finally {
        loading.value = false
      }
    }

    const loadChapters = async () => {
      if (!selectedSubject.value) {
        chapters.value = []
        return
      }
      loading.value = true
      try {
        const response = await axios.get(`/api/subjects/${selectedSubject.value}/chapters`)
        chapters.value = response.data
        selectedChapter.value = ''
        selectedQuiz.value = ''
      } catch (error) {
        console.error('Error loading chapters:', error)
        alert('Failed to load chapters. Please try again later.')
      } finally {
        loading.value = false
      }
    }

    const loadQuizzes = async () => {
      if (!selectedChapter.value) {
        quizzes.value = []
        return
      }
      loading.value = true
      try {
        const response = await axios.get(`/api/chapters/${selectedChapter.value}/quizzes`)
        quizzes.value = response.data
        selectedQuiz.value = ''
      } catch (error) {
        console.error('Error loading quizzes:', error)
        alert('Failed to load quizzes. Please try again later.')
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const formatDuration = (duration) => {
      const [hours, minutes] = duration.split(':')
      return `${hours} hr ${minutes} min`
    }

    const startQuiz = () => {
      if (selectedQuiz.value) {
        router.push(`/quiz/${selectedQuiz.value}`)
      }
    }
    const handleQuizStart = async () => {
      if (selectedQuiz.value) {
        loading.value = true
        try {
          // Make API call to backend to update database
          await axios.post('/api/quiz-starts', {
            quiz_id: selectedQuiz.value
          })
          router.push('/user-dashboard')
        } catch (error) {
          console.error('Error starting quiz:', error)
          alert('Failed to start quiz. Please try again later.')
        } finally {
          loading.value = false
        }
      }
    }
    onMounted(() => {
      loadSubjects()
    })

    return {
      subjects,
      chapters,
      quizzes,
      selectedSubject,
      selectedChapter,
      selectedQuiz,
      loading,
      loadChapters,
      loadQuizzes,
      formatDate,
      formatDuration,
      startQuiz,
      handleQuizStart
    }
  }
}
</script>

<style scoped>
.quiz-selector {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  font-size: 18px;
  color: #888;
}

.selector-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.select-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 16px;
}

select:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.take-quiz-btn {
  padding: 12px 24px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.take-quiz-btn:hover {
  background-color: #45a049;
}

.take-quiz-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
