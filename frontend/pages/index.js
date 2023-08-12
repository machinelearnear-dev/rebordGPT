import Head from 'next/head'
import { Inter } from 'next/font/google'
import { Hero } from '../components/hero/hero'
import { ThemeProvider } from 'next-themes'
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { useTheme } from 'next-themes'

export default function Home() {
  return (
    <Hero />
  )
}