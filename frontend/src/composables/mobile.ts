import { computed } from "vue";
import { useDisplay } from "vuetify";

export function useMobile() {
  const { xs, sm } = useDisplay();
  // eslint-disable-next-line @typescript-eslint/no-unsafe-return,@typescript-eslint/no-unsafe-member-access
  const isPhone = computed((): boolean => xs.value);
  // eslint-disable-next-line @typescript-eslint/no-unsafe-return,@typescript-eslint/no-unsafe-member-access
  const isTablet = computed((): boolean => sm.value);
  const isMobile = computed((): boolean => isPhone.value || isTablet.value);

  return {
    isPhone,
    isMobile,
  };
}
