import * as React from "react"

import { cn } from "@/lib/utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "h-9 w-full min-w-0 rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 px-3 py-1 text-base shadow-xs transition-all duration-200 outline-none placeholder:text-slate-400 dark:placeholder:text-slate-500 selection:bg-blue-200 dark:selection:bg-blue-900 selection:text-slate-900 dark:selection:text-slate-100 file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-slate-900 dark:file:text-slate-100 disabled:pointer-events-none disabled:cursor-not-allowed disabled:bg-slate-50 dark:disabled:bg-slate-900 disabled:text-slate-500 dark:disabled:text-slate-600 md:text-sm hover:border-blue-500 dark:hover:border-blue-400",
        "focus-visible:border-blue-500 dark:focus-visible:border-blue-400 focus-visible:ring-blue-500/50 dark:focus-visible:ring-blue-400/50 focus-visible:ring-[3px]",
        "aria-invalid:ring-red-500/20 dark:aria-invalid:ring-red-400/40 aria-invalid:border-red-500 dark:aria-invalid:border-red-400",
        className
      )}
      {...props}
    />
  )
}

export { Input }
