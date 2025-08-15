import type { AppProps } from 'next/app'
import { useEffect } from 'react'
import { useRouter } from 'next/router'
import '../styles/globals.css'
import { authHelpers } from '../lib/supabaseClient'

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter()

  useEffect(() => {
    // Listen for auth changes
    const { data: { subscription } } = authHelpers.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_IN') {
        // User signed in
        if (router.pathname === '/login') {
          router.push('/dashboard')
        }
      } else if (event === 'SIGNED_OUT') {
        // User signed out
        if (router.pathname.startsWith('/dashboard')) {
          router.push('/')
        }
      }
    })

    return () => subscription.unsubscribe()
  }, [router])

  return <Component {...pageProps} />
}