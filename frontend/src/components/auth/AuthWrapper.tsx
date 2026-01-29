import { CheckCircle2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";

interface AuthWrapperProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
}

/**
 * AuthWrapper - Elegant wrapper component for authentication pages
 * Features:
 * - Glass-morphism card design
 * - Centered layout with responsive padding
 * - App branding at the top
 * - Supports optional title and description
 * - Works seamlessly across mobile, tablet, and desktop
 */
export function AuthWrapper({ children, title, description }: AuthWrapperProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center p-4">
      {/* Background Gradient Orbs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full filter blur-3xl opacity-20 animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full filter blur-3xl opacity-20 animate-pulse" style={{ animationDelay: '1s' }} />
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Logo / App Name */}
        <div className="flex flex-col items-center mb-8">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle2 className="h-10 w-10 text-primary" />
            <span className="text-2xl font-bold">TaskFlow</span>
          </div>
          {title && (
            <h1 className="text-3xl font-bold text-center mt-4">{title}</h1>
          )}
          {description && (
            <p className="text-muted-foreground text-center mt-2">{description}</p>
          )}
        </div>

        {/* Glass-morphism Card */}
        <Card className="border-border/50 shadow-2xl backdrop-blur-sm bg-white/80 dark:bg-gray-900/80">
          <CardContent className="pt-6">
            {children}
          </CardContent>
        </Card>

        {/* Footer */}
        <p className="text-center text-sm text-muted-foreground mt-6">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
}
