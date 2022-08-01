export const mobileMixin = {
  computed: {
    isPhone(): boolean {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return
      return this.$vuetify.display.xs;
    },
    isTablet(): boolean {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return
      return this.$vuetify.display.sm;
    },
    isMobile(): boolean {
      // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
      return this.isPhone || this.isTablet;
    },
  },
};
