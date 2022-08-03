<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4" cols="12">
        <v-form v-if="!isLoggedIn" ref="form" v-model="valid" lazy-validation @submit.prevent="onSubmit">
          <v-text-field
            v-model="username"
            variant="outlined"
            label="Username"
            :rules="[rules.required]"
            @keyup.enter="onSubmit"
          ></v-text-field>
          <v-text-field
            v-model="password"
            variant="outlined"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required]"
            :type="showPassword ? 'text' : 'password'"
            label="Password"
            @click:append="showPassword = !showPassword"
            @keyup.enter="onSubmit"
          ></v-text-field>
          <div class="d-flex justify-space-around align-center flex-column flex-md-row">
            <v-btn color="primary" :disabled="!valid" @click="onSubmit">Login</v-btn>
          </div>
        </v-form>
        <p v-if="isLoggedIn">You are already logged in.</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import { rules } from "../helpers";
import { useAuthStore } from "../stores/auth";

export default defineComponent({
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      showPassword: false,
      valid: false,
      rules: rules,
    };
  },
  computed: {
    isLoggedIn() {
      const { user } = useAuthStore();
      return user.isLoggedIn;
    },
  },
  methods: {
    async isValid(): Promise<boolean> {
      const result = await this.$refs.form.validate();
      const valid: boolean = result.valid;
      return valid;
    },
    async onSubmit() {
      if (!(await this.isValid())) {
        return;
      }
      const { login } = useAuthStore();
      try {
        await login(this.username, this.password);
      } catch (error) {
        console.log(error);
        this.$toast.error(error.response.data.detail);
      }
    },
  },
});
</script>
