<template>
  <div class="register-link">
    <button @click="$router.push('/register')" class="register-btn">Register</button>
  </div>
  <div class="login-container">
    <div class="login-box">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text"
            id="username"
            v-model="username"
            required
            placeholder="Enter username"
          >
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password" 
            v-model="password"
            required
            placeholder="Enter password"
          >
        </div>
        <button type="submit" class="login-btn">Login</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: '',
      error: null,
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('/api/login', {
          username: this.username,
          password: this.password,
        });

        // Store the token
        localStorage.setItem('token', response.data.access_token);

        // Redirect based on is_admin flag
        if (response.data.is_admin) {
          this.$router.push('/admin/dashboard');
        } else {
          this.$router.push('/user/dashboard');
        }
      } catch (err) {
        this.error =
          err.response?.data?.error || 'Login failed. Please try again.';
      }
    },
  },
};
</script>

<style scoped>
/* Container styling */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

/* Login box styling */
.login-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

/* Form group styling */
.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  text-align: left;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

/* Login button styling */
.login-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

.login-btn:hover {
  background-color: #34495e;
}

/* Error message styling */
.error {
  color: #dc3545;
  margin-top: 1rem;
  font-size: 0.9rem;
}

/* Register button container styling */
.register-link {
  position: absolute;
  top: 1rem;
  right: 1rem;
}

/* Register button styling */
.register-btn {
  background-color: #34495e;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
}

.register-btn:hover {
  background-color: #34495e;
}
</style>
