<template>
    <div class="register-container">
      <h2>User Registration</h2>
      <form @submit.prevent="register" class="register-form">
        <div class="form-group">
          <label for="username">Username:</label>
          <input 
            type="text"
            id="username"
            v-model="formData.username"
            required
          >
        </div>
  
        <div class="form-group">
          <label for="password">Password:</label>
          <input
            type="password"
            id="password"
            v-model="formData.password"
            required
          >
        </div>
  
        <div class="form-group">
          <label for="dob">Date of Birth:</label>
          <input
            type="date"
            id="dob"
            v-model="formData.dob"
            required
          >
        </div>
  
        <div class="form-group">
          <label for="qualification">Qualification:</label>
          <input
            type="text"
            id="qualification"
            v-model="formData.qualification"
            required
          >
        </div>
  
        <button type="submit">Register</button>
      </form>
  
      <div v-if="error" class="error">
        {{ error }}
      </div>
  
      <!-- Popup for successful registration -->
      <div v-if="showPopup" class="popup-overlay">
        <div class="popup">
          <p>Registration Successful!</p>
          <button @click="closePopup">OK</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserRegister',
    data() {
      return {
        formData: {
          username: '',
          password: '',
          dob: '',
          qualification: '',
        },
        error: null,
        showPopup: false, // State to show or hide the popup
      };
    },
    methods: {
      async register() {
        try {
          // Format date to DD/MM/YYYY
          const dateObj = new Date(this.formData.dob);
          const formattedDate = `${String(dateObj.getDate()).padStart(2, '0')}/${String(
            dateObj.getMonth() + 1
          ).padStart(2, '0')}/${dateObj.getFullYear()}`;
  
          const response = await axios.post('api/register', {
            username: this.formData.username,
            password: this.formData.password,
            is_admin: false,
            dob: formattedDate,
            qualification: this.formData.qualification,
          });
  
          if (response.status === 201) {
            this.showPopup = true; // Show the popup on successful registration
          }
        } catch (err) {
          this.error = err.response?.data?.error || 'Registration failed';
        }
      },
      closePopup() {
        this.showPopup = false; // Hide the popup
        this.$router.push('/login'); // Redirect to login after closing the popup
      },
    },
  };
  </script>
  
  <style scoped>
  .register-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .register-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  
  input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    padding: 10px;
    background-color: #34495e;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #2c3e50;
  }
  
  .error {
    color: red;
    margin-top: 10px;
    text-align: center;
  }
  
  /* Popup styling */
  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .popup {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    text-align: center;
  }
  
  .popup p {
    font-size: 1.2rem;
    margin-bottom: 15px;
  }
  
  .popup button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .popup button:hover {
    background-color: #0056b3;
  }
  </style>
  