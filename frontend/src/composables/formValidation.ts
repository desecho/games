import { ref } from "vue";

import { FormValidationResult } from "./types";

export function useFormValidation() {
  // Not sure how to type this
  const form = ref(null);

  async function isValid(): Promise<boolean> {
    const value = form.value;
    // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
    if (value) {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      const result = (await value.validate()) as FormValidationResult;
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
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
