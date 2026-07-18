import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertTriangle, RefreshCcw } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  private handleRetry = () => {
    this.setState({ hasError: false, error: undefined });
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center p-8 bg-zinc-900/50 rounded-xl border border-red-500/20 m-4 shadow-lg text-center min-h-[300px]">
          <div className="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mb-6">
            <AlertTriangle className="w-8 h-8 text-red-500" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">Component Failure</h2>
          <p className="text-zinc-400 max-w-md mb-8">
            This module encountered an unexpected error and has been isolated to protect the rest of the application.
          </p>
          <div className="bg-black/50 p-4 rounded-lg w-full max-w-2xl overflow-auto text-left mb-8 border border-red-500/10">
            <code className="text-red-400 text-sm font-mono whitespace-pre-wrap">
              {this.state.error?.message || "Unknown error occurred"}
            </code>
          </div>
          <Button onClick={this.handleRetry} variant="outline" className="border-red-500/30 text-red-400 hover:bg-red-500/10 gap-2">
            <RefreshCcw className="w-4 h-4" />
            Retry Component
          </Button>
        </div>
      );
    }

    return this.props.children;
  }
}
