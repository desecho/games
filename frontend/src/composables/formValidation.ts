import { ref } from "vue";

export function useFormValidation() {
  const form = ref<HTMLFormElement | null>(null);

  async function isValid(): Promise<boolean> {
    const result = await form.value!.validate();
    const valid: boolean = result.valid;
    return valid;
  }

  return {
    form,
    isValid,
  };
}
