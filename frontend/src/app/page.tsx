'use client';

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  CheckCircle2,
  Sparkles,
  Zap,
  Layout,
  BrainCircuit,
  Shield,
  Clock,
  ArrowRight,
  Play,
  Github,
  Twitter,
  Linkedin,
  Heart,
} from "lucide-react";
import { ThemeToggle } from "@/components/shared/ThemeToggle";
import { motion } from "motion/react";

// Floating Orb Component
function FloatingOrb({ className, delay = 0 }: { className?: string; delay?: number }) {
  return (
    <motion.div
      className={`absolute rounded-full filter blur-3xl ${className}`}
      animate={{
        y: [0, -30, 0],
        x: [0, 15, 0],
        scale: [1, 1.1, 1],
      }}
      transition={{
        duration: 8,
        repeat: Infinity,
        repeatType: "reverse",
        ease: "easeInOut",
        delay,
      }}
    />
  );
}

// Task Card Component for Dashboard Mockup
function TaskCard({
  title,
  priority,
  delay = 0
}: {
  title: string;
  priority: "high" | "medium" | "low";
  delay?: number;
}) {
  const priorityColors = {
    high: "bg-rose-100 text-rose-600 dark:bg-rose-900/30 dark:text-rose-400",
    medium: "bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400",
    low: "bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400",
  };

  return (
    <motion.div
      className="bg-white dark:bg-gray-800 rounded-xl p-3 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-all duration-300 cursor-pointer group"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
      whileHover={{ y: -2, scale: 1.02 }}
    >
      <div className="flex items-start gap-2">
        <div className="w-4 h-4 rounded border-2 border-gray-300 dark:border-gray-600 mt-0.5 group-hover:border-indigo-500 transition-colors" />
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-700 dark:text-gray-200 leading-tight">
            {title}
          </p>
          <span className={`inline-block mt-1.5 px-2 py-0.5 rounded-full text-xs font-medium ${priorityColors[priority]}`}>
            {priority}
          </span>
        </div>
      </div>
    </motion.div>
  );
}

// Dashboard Mockup Component
function DashboardMockup() {
  const columns = [
    {
      title: "To Do",
      color: "bg-gray-100 dark:bg-gray-800/50",
      tasks: [
        { title: "Design new landing page", priority: "high" as const },
        { title: "Update documentation", priority: "low" as const },
        { title: "Review pull requests", priority: "medium" as const },
      ],
    },
    {
      title: "In Progress",
      color: "bg-indigo-50 dark:bg-indigo-900/20",
      tasks: [
        { title: "Implement dark mode", priority: "high" as const },
        { title: "Write unit tests", priority: "medium" as const },
      ],
    },
    {
      title: "Done",
      color: "bg-emerald-50 dark:bg-emerald-900/20",
      tasks: [
        { title: "Set up CI/CD pipeline", priority: "high" as const },
        { title: "Create user auth flow", priority: "high" as const },
        { title: "Design system setup", priority: "medium" as const },
      ],
    },
  ];

  return (
    <motion.div
      className="relative w-full max-w-5xl mx-auto"
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5, duration: 0.8, ease: "easeOut" }}
    >
      {/* Browser Chrome */}
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl shadow-indigo-500/10 dark:shadow-indigo-500/5 border border-gray-200 dark:border-gray-700 overflow-hidden">
        {/* Title Bar */}
        <div className="bg-gray-50 dark:bg-gray-800 px-4 py-3 flex items-center gap-2 border-b border-gray-200 dark:border-gray-700">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-400" />
            <div className="w-3 h-3 rounded-full bg-amber-400" />
            <div className="w-3 h-3 rounded-full bg-emerald-400" />
          </div>
          <div className="flex-1 flex justify-center">
            <div className="bg-gray-200 dark:bg-gray-700 rounded-lg px-4 py-1.5 text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2">
              <Shield className="w-3 h-3" />
              taskflow.app/dashboard
            </div>
          </div>
        </div>

        {/* Dashboard Content */}
        <div className="p-6 bg-gradient-to-br from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
          {/* Dashboard Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">My Projects</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">8 tasks remaining</p>
            </div>
            <motion.button
              className="bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 shadow-md"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Zap className="w-4 h-4" />
              Add Task
            </motion.button>
          </div>

          {/* Kanban Board */}
          <div className="grid grid-cols-3 gap-4">
            {columns.map((column, colIndex) => (
              <motion.div
                key={column.title}
                className={`${column.color} rounded-xl p-4`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 + colIndex * 0.1, duration: 0.5 }}
              >
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-semibold text-gray-700 dark:text-gray-200 text-sm">
                    {column.title}
                  </h4>
                  <span className="bg-white dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-xs font-medium px-2 py-1 rounded-full">
                    {column.tasks.length}
                  </span>
                </div>
                <div className="space-y-3">
                  {column.tasks.map((task, taskIndex) => (
                    <TaskCard
                      key={task.title}
                      title={task.title}
                      priority={task.priority}
                      delay={0.7 + colIndex * 0.1 + taskIndex * 0.05}
                    />
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Decorative Elements */}
      <div className="absolute -bottom-4 -right-4 w-32 h-32 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full filter blur-2xl" />
      <div className="absolute -top-4 -left-4 w-24 h-24 bg-gradient-to-br from-indigo-500/20 to-blue-500/20 rounded-full filter blur-2xl" />
    </motion.div>
  );
}

// Feature Card Component
function FeatureCard({
  icon: Icon,
  title,
  description,
  delay = 0,
}: {
  icon: React.ElementType;
  title: string;
  description: string;
  delay?: number;
}) {
  return (
    <motion.div
      className="group relative bg-white dark:bg-gray-800/50 rounded-3xl p-8 border border-gray-100 dark:border-gray-700/50 shadow-sm hover:shadow-xl transition-all duration-500"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ delay, duration: 0.5, ease: "easeOut" }}
      whileHover={{ y: -8, scale: 1.02 }}
    >
      {/* Gradient Background on Hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 via-purple-500/5 to-pink-500/5 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

      {/* Icon Container */}
      <motion.div
        className="relative w-14 h-14 bg-gradient-to-br from-indigo-100 to-purple-100 dark:from-indigo-900/50 dark:to-purple-900/50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300"
        whileHover={{ rotate: 5 }}
      >
        <Icon className="w-7 h-7 text-indigo-600 dark:text-indigo-400" />
      </motion.div>

      {/* Content */}
      <h3 className="relative text-xl font-semibold text-gray-900 dark:text-white mb-3">
        {title}
      </h3>
      <p className="relative text-gray-600 dark:text-gray-400 leading-relaxed">
        {description}
      </p>

      {/* Arrow indicator */}
      <motion.div
        className="relative mt-4 flex items-center text-indigo-600 dark:text-indigo-400 font-medium text-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        initial={{ x: -10 }}
        whileHover={{ x: 0 }}
      >
        Learn more <ArrowRight className="w-4 h-4 ml-1" />
      </motion.div>
    </motion.div>
  );
}

// Main Page Component
export default function Home() {
  const features = [
    {
      icon: Layout,
      title: "Flexible Views",
      description: "Switch between Kanban boards, lists, and calendar views. Organize your work the way that suits you best.",
    },
    {
      icon: BrainCircuit,
      title: "AI Assistance",
      description: "Smart task suggestions, automatic prioritization, and intelligent reminders powered by advanced AI.",
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Blazing fast performance with real-time sync across all your devices. No more waiting.",
    },
    {
      icon: Sparkles,
      title: "Beautiful & Clean",
      description: "A premium aesthetic that inspires productivity. Dark and light modes with stunning animations.",
    },
    {
      icon: Shield,
      title: "Secure & Private",
      description: "End-to-end encryption for your data. Your tasks stay private and secure, always.",
    },
    {
      icon: Clock,
      title: "Time Tracking",
      description: "Built-in time tracking and analytics. Understand where your time goes and optimize your workflow.",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-gray-950 dark:via-gray-900 dark:to-indigo-950/30 transition-colors duration-500">
      {/* Floating Background Orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <FloatingOrb
          className="top-[10%] left-[10%] w-96 h-96 bg-indigo-400/20 dark:bg-indigo-600/10"
          delay={0}
        />
        <FloatingOrb
          className="top-[30%] right-[5%] w-80 h-80 bg-purple-400/20 dark:bg-purple-600/10"
          delay={2}
        />
        <FloatingOrb
          className="bottom-[20%] left-[20%] w-72 h-72 bg-pink-400/15 dark:bg-pink-600/10"
          delay={4}
        />
        <FloatingOrb
          className="bottom-[10%] right-[15%] w-64 h-64 bg-rose-400/15 dark:bg-rose-600/10"
          delay={1}
        />
      </div>

      {/* Fixed Glassmorphic Header */}
      <motion.header
        className="fixed top-0 left-0 right-0 z-50"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <nav className="mx-4 mt-4 rounded-2xl bg-white/70 dark:bg-gray-900/70 backdrop-blur-xl border border-gray-200/50 dark:border-gray-700/50 shadow-lg shadow-gray-900/5 dark:shadow-gray-900/30">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-2.5 group">
              <motion.div
                className="relative"
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg blur-sm opacity-50 group-hover:opacity-75 transition-opacity" />
                <div className="relative bg-gradient-to-r from-indigo-500 to-purple-500 p-2 rounded-lg">
                  <CheckCircle2 className="h-5 w-5 text-white" />
                </div>
              </motion.div>
              <span className="text-xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 bg-clip-text text-transparent">
                TaskFlow
              </span>
            </Link>

            {/* Navigation Items */}
            <div className="flex items-center gap-3">
              <Link href="/sign-in">
                <Button variant="ghost" size="sm" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
                  Sign In
                </Button>
              </Link>
              <Link href="/sign-up">
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    size="sm"
                    className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white border-0 shadow-md hover:shadow-lg hover:opacity-90 transition-all"
                  >
                    Get Started
                  </Button>
                </motion.div>
              </Link>
              <ThemeToggle />
            </div>
          </div>
        </nav>
      </motion.header>

      {/* Hero Section */}
      <main className="relative pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Badge */}
          <motion.div
            className="flex justify-center mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <div className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 dark:from-indigo-900/50 dark:to-purple-900/50 px-5 py-2.5 text-sm font-medium text-indigo-700 dark:text-indigo-300 border border-indigo-200/50 dark:border-indigo-700/50">
              <Sparkles className="h-4 w-4" />
              <span>AI-Powered Productivity</span>
              <span className="bg-indigo-500 text-white text-xs px-2 py-0.5 rounded-full">New</span>
            </div>
          </motion.div>

          {/* Main Headline */}
          <motion.div
            className="text-center mb-8"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.6 }}
          >
            <h1 className="text-5xl sm:text-6xl lg:text-7xl xl:text-8xl font-extrabold tracking-tight leading-[1.1] mb-6">
              <span className="bg-gradient-to-r from-gray-900 via-gray-700 to-gray-900 dark:from-white dark:via-gray-200 dark:to-white bg-clip-text text-transparent">
                Organize Your Life,
              </span>
              <br />
              <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 bg-clip-text text-transparent">
                Beautifully
              </span>
            </h1>
          </motion.div>

          {/* Subheadline */}
          <motion.p
            className="max-w-3xl mx-auto text-center text-lg sm:text-xl lg:text-2xl text-gray-600 dark:text-gray-400 mb-12 leading-relaxed"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.6 }}
          >
            A premium task management experience with{" "}
            <span className="text-indigo-600 dark:text-indigo-400 font-medium">elegant design</span>,{" "}
            <span className="text-purple-600 dark:text-purple-400 font-medium">AI-powered intelligence</span>, and{" "}
            <span className="text-pink-600 dark:text-pink-400 font-medium">delightful simplicity</span>.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            <Link href="/sign-up">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  size="lg"
                  className="text-lg px-8 py-7 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 text-white border-0 shadow-xl shadow-indigo-500/25 hover:shadow-2xl hover:shadow-indigo-500/30 transition-all duration-300 rounded-2xl"
                >
                  <Zap className="mr-2 h-5 w-5" />
                  Start Free Forever
                </Button>
              </motion.div>
            </Link>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                size="lg"
                variant="outline"
                className="text-lg px-8 py-7 rounded-2xl border-2 border-gray-200 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-600 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm"
              >
                <Play className="mr-2 h-5 w-5" />
                Watch Demo
              </Button>
            </motion.div>
          </motion.div>

          {/* Dashboard Mockup */}
          <DashboardMockup />
        </div>
      </main>

      {/* Features Section */}
      <section className="relative py-32 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Section Header */}
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-block text-sm font-semibold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider mb-4">
              Features
            </span>
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mb-6">
              Everything you need to{" "}
              <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                stay productive
              </span>
            </h2>
            <p className="max-w-2xl mx-auto text-lg text-gray-600 dark:text-gray-400">
              Powerful features designed with simplicity in mind. Get more done with less effort.
            </p>
          </motion.div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <FeatureCard
                key={feature.title}
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
                delay={index * 0.1}
              />
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-24 px-6">
        <motion.div
          className="max-w-5xl mx-auto bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 rounded-3xl p-12 md:p-16 text-center relative overflow-hidden"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 left-0 w-full h-full bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC40Ij48cGF0aCBkPSJNMzYgMzRjMC0yLjIwOS0xLjc5MS00LTQtNHMtNCAxLjc5MS00IDQgMS43OTEgNCA0IDQgNC0xLjc5MSA0LTR6bTAtMThjMC0yLjIwOS0xLjc5MS00LTQtNHMtNCAxLjc5MS00IDQgMS43OTEgNCA0IDQgNC0xLjc5MSA0LTR6bTE4IDBjMC0yLjIwOS0xLjc5MS00LTQtNHMtNCAxLjc5MS00IDQgMS43OTEgNCA0IDQgNC0xLjc5MSA0LTR6bS0xOCAxOGMwLTIuMjA5LTEuNzkxLTQtNC00cy00IDEuNzkxLTQgNCAxLjc5MSA0IDQgNCA0LTEuNzkxIDQtNHptMTggMGMwLTIuMjA5LTEuNzkxLTQtNC00cy00IDEuNzkxLTQgNCAxLjc5MSA0IDQgNCA0LTEuNzkxIDQtNHptLTE4IDE4YzAtMi4yMDktMS43OTEtNC00LTRzLTQgMS43OTEtNCA0IDEuNzkxIDQgNCA0IDQtMS43OTEgNC00em0xOCAwYzAtMi4yMDktMS43OTEtNC00LTRzLTQgMS43OTEtNCA0IDEuNzkxIDQgNCA0IDQtMS43OTEgNC00eiIvPjwvZz48L2c+PC9zdmc+')] bg-repeat" />
          </div>

          <div className="relative">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-6">
              Ready to transform your productivity?
            </h2>
            <p className="text-lg text-white/80 mb-10 max-w-2xl mx-auto">
              Join thousands of users who have already discovered a better way to manage their tasks.
            </p>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link href="/sign-up">
                <Button
                  size="lg"
                  className="text-lg px-10 py-7 bg-white text-indigo-600 hover:bg-gray-100 shadow-xl rounded-2xl font-semibold"
                >
                  Get Started Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </motion.div>
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="relative border-t border-gray-200 dark:border-gray-800 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-16">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 md:gap-8">
            {/* Logo & Description */}
            <div className="md:col-span-1">
              <Link href="/" className="flex items-center gap-2.5 mb-4">
                <div className="bg-gradient-to-r from-indigo-500 to-purple-500 p-2 rounded-lg">
                  <CheckCircle2 className="h-5 w-5 text-white" />
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  TaskFlow
                </span>
              </Link>
              <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-6">
                Beautiful task management for people who care about both productivity and aesthetics.
              </p>
              {/* Social Icons */}
              <div className="flex items-center gap-3">
                {[Github, Twitter, Linkedin].map((Icon, index) => (
                  <motion.a
                    key={index}
                    href="#"
                    className="w-10 h-10 rounded-xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-indigo-100 dark:hover:bg-indigo-900/50 hover:text-indigo-600 dark:hover:text-indigo-400 transition-all"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Icon className="w-5 h-5" />
                  </motion.a>
                ))}
              </div>
            </div>

            {/* Links */}
            {[
              {
                title: "Product",
                links: ["Features", "Pricing", "Integrations", "Changelog"],
              },
              {
                title: "Company",
                links: ["About", "Blog", "Careers", "Press"],
              },
              {
                title: "Resources",
                links: ["Documentation", "Help Center", "Contact", "Privacy"],
              },
            ].map((section) => (
              <div key={section.title}>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-4">
                  {section.title}
                </h4>
                <ul className="space-y-3">
                  {section.links.map((link) => (
                    <li key={link}>
                      <a
                        href="#"
                        className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors text-sm"
                      >
                        {link}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Bottom Bar */}
          <div className="mt-16 pt-8 border-t border-gray-200 dark:border-gray-800 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              &copy; {new Date().getFullYear()} TaskFlow. All rights reserved.
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400 flex items-center gap-1.5">
              Made with <Heart className="w-4 h-4 text-rose-500 fill-rose-500" /> by the TaskFlow team
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
