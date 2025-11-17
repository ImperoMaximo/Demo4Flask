import { defineStore } from 'pinia'

export const useSubmissionStore = defineStore('submission', {
  state: () => ({
    submissions: JSON.parse(localStorage.getItem('submissions') || '[]') || []
  }),
  actions: {
    addSubmission(text) {
      const item = { id: Date.now(), text }
      this.submissions.unshift(item)
      localStorage.setItem('submissions', JSON.stringify(this.submissions))
    },
    clear() {
      this.submissions = []
      localStorage.removeItem('submissions')
    }
  }
})
