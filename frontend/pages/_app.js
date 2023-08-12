import 'styles/globals.css'
import { ThemeProvider } from 'next-themes'
import { Layout } from 'components/layout/layout'

export default function App({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  )
}
