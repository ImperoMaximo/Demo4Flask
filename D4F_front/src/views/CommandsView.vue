<script setup>
import { ref } from 'vue'
import { useSubmissionStore } from '@/stores/submission'

const text = ref('')
const store = useSubmissionStore()

function submit() {
  if (!text.value.trim()) return
  store.addSubmission(text.value.trim())
  text.value = ''
  alert('Texte enregistré')
}
</script>

<template>
  <div>
    <h2>Envoyer un texte</h2>
    <p>Entrez votre texte puis cliquez sur Envoyer.</p>
    <textarea v-model="text" rows="5" style="width:100%"></textarea>
    <div style="margin-top: 1rem;">
      <button @click="submit">Envoyer</button>
    </div>

    <div v-if="store.submissions.length" style="margin-top:1rem;">
      <h3>Textes enregistrés</h3>
      <ul>
        <li v-for="(s, i) in store.submissions" :key="i">{{ s }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
textarea { font-family: inherit; }
button { padding: 0.5rem 1rem; }
</style>
