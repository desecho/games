import { computed } from "vue";
import { useDisplay } from "vuetify";

export function useMobile() {
  const { xs, sm } = useDisplay();
  const isPhone = computed((): boolean => xs.value);
  const isTablet = computed((): boolean => sm.value);
  const isMobile = computed((): boolean => isPhone.value || isTablet.value);

  return {
    isPhone,
    isMobile,
  };
}
