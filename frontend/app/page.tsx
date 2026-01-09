'use client';

import Link from 'next/link';
import { ArrowRight, Sparkles, CheckCircle2 } from 'lucide-react';

export default function WelcomeLandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-teal-50 to-cyan-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="fixed top-0 w-full bg-white/70 dark:bg-slate-900/70 backdrop-blur-lg border-b border-slate-200/70 dark:border-slate-800/50 z-50">
        <div className="max-w-7xl mx-auto px-5 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-xl flex items-center justify-center shadow-md">
              <CheckCircle2 className="h-6 w-6 text-white" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent">
              FlowTask
            </span>
          </div>

          <div className="flex items-center gap-6">
            <Link 
              href="/login"
              className="text-slate-700 dark:text-slate-300 hover:text-teal-600 font-medium transition"
            >
              Sign in
            </Link>
            <Link
              href="/signup"
              className="px-6 py-2.5 bg-gradient-to-r from-teal-600 to-cyan-600 text-white rounded-lg font-medium hover:from-teal-700 hover:to-cyan-700 shadow-md hover:shadow-lg transition"
            >
              Get Started →
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="pt-32 pb-20 px-5 text-center">
        <div className="max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-5 py-2 bg-teal-100 dark:bg-teal-950/40 rounded-full mb-8">
            <Sparkles className="h-4 w-4 text-teal-600" />
            <span className="text-sm font-medium text-teal-700 dark:text-teal-300">
              Simple • Beautiful • Productive
            </span>
          </div>

          <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold tracking-tight mb-8 bg-gradient-to-r from-slate-900 via-teal-700 to-cyan-700 bg-clip-text text-transparent dark:from-white dark:via-teal-400 dark:to-cyan-400">
            Get your life together,
            <br className="hidden sm:block" />
            one task at a time
          </h1>

          <p className="text-xl md:text-2xl text-slate-700 dark:text-slate-300 mb-12 max-w-3xl mx-auto leading-relaxed">
            The cleanest way to organize your day, focus on what matters, and actually finish things.
          </p>

          <div className="flex flex-col sm:flex-row gap-5 justify-center">
            <Link
              href="/signup"
              className="group px-10 py-5 bg-gradient-to-r from-teal-600 to-cyan-600 text-white rounded-xl font-semibold text-lg shadow-xl hover:shadow-2xl hover:from-teal-700 hover:to-cyan-700 transition transform hover:scale-[1.02] flex items-center justify-center gap-3"
            >
              Start for Free
              <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Link>

            <Link
              href="/login"
              className="px-10 py-5 bg-white dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-semibold text-lg border border-slate-200 dark:border-slate-700 hover:border-teal-400 transition shadow-sm hover:shadow-md"
            >
              I already have an account
            </Link>
          </div>
        </div>
      </main>

      {/* You can add features section, testimonials etc here */}
    </div>
  );
}