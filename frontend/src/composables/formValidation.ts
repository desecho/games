import { ref } from "vue";

export function useFormValidation() {
  const form = ref<HTMLFormElement | null>(null);

  async function isValid(): Promise<boolean> {
    const value = form.value;
    if (value) {
      const result = await value.validate();
      const valid: boolean = result.valid;
      return valid;
    }
    return false;
  }

  return {
    form,
    isValid,
  };
}
