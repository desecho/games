<template>
  <v-container>
    <v-row>
      <v-col cols="9">
        <p>Create game lists like "Want to Play", "Playing", "Beaten", "On Hold".</p>
        <p>Currently only the "PC (Microsoft Windows)" platform is supported.</p>
        <br />
        <h3>Features</h3>
        <ul>
          <li>Search for games to add to your collection</li>
          <li>Add custom order your lists</li>
          <li>Share your lists online</li>
          <li>Privacy settings</li>
        </ul>
        <br />
        <h3>Limitations</h3>
        <ul>
          <li>Adding custom order for your lists is not available on mobile</li>
        </ul>
        <br />
        <h3>APIs used</h3>
        <ul>
          <li><a href="https://www.igdb.com/" target="_blank">IGDB</a></li>
        </ul>
        <br />
        <h3>Import/Export data</h3>
        <p>If you would like to import or export data, please <a :href="`mailto:${email}`">email me</a>.</p>
        <br />
        <h3>Source code</h3>
        <p>The source code is available <a href="https://github.com/desecho/games" target="_blank">on GitHub</a>.</p>
        <br />
        <h3>Contact info</h3>
        <p>
          If you have problems with account activation or other issues, questions or feedback please email me at
          <a :href="`mailto:${email}`">{{ email }}</a
          >.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { Email } from "../const";

const email = Email;
</script>
