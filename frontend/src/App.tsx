// ===================
// ©AngelaMos | 2026
// App.tsx
// ===================

import { QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider } from 'react-router-dom'
import { Toaster } from 'sonner'
import { queryClient } from '@/core/api'
import { router } from '@/core/app/router'
import { AIChatbot } from '@/core/app/AIChatbot'


export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <AIChatbot projectName="Honeypot Network" />
        <Toaster position="bottom-right" theme="dark" richColors />
    </QueryClientProvider>
  )
}
