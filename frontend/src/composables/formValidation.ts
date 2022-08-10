import { ref } from "vue";

import type { FormValidationResult } from "./types";
import type { Ref } from "vue";

export function useFormValidation(): {
  form: Ref<null>;
  isValid: () => Promise<boolean>;
} {
  // Not sure how to type this
  const form = ref(null);

  async function isValid(): Promise<boolean> {
    const value = form.value;
    // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
    if (value !== null) {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-call
      const result = (await value.validate()) as FormValidationResult;
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
