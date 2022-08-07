import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-default.css";

export const $toast = useToast({
  position: "bottom-right",
  duration: 1500,
});
