"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PlusCircle, History, Settings, LogOut } from "lucide-react";
import Link from "next/link";
import CopyForm from "@/components/copy-form";
import CopyHistory from "@/components/copy-history";
import { isAuthenticated, logout } from "@/lib/auth-utils";

export default function DashboardPage() {
  const router = useRouter();
  const [authChecked, setAuthChecked] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [history, setHistory] = useState([
    {
      id: "1",
      productName: "UltraBoost Running Shoes",
      createdAt: "2023-04-15T10:30:00Z",
      preview:
        "Transform your running experience with UltraBoost Running Shoes...",
      content: "# UltraBoost Running Shoes - Transform Your Experience\n\n...",
    },
    // other sample entries...
  ]);

  useEffect(() => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      router.push("/login");
    }
    setAuthChecked(true);
    setIsLoading(false);
  }, [router]);

  const handleLogout = () => {
    logout();
  };

  const addToHistory = (entry: {
    id: string;
    productName: string;
    createdAt: string;
    preview: string;
    content: string;
  }) => {
    setHistory((prev) => [entry, ...prev]);
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">Loading...</div>
      </div>
    );
  }

  if (!authChecked) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-10 border-b bg-background px-4 lg:px-6">
        <div className="flex h-14 items-center justify-between">
          <Link href="/dashboard" className="flex items-center font-semibold">
            <span className="text-xl">CopyGenius</span>
          </Link>
          <nav className="flex items-center gap-4 sm:gap-6">
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              <LogOut className="mr-2 h-4 w-4" />
              Logout
            </Button>
          </nav>
        </div>
      </header>
      <main className="flex-1 p-4 md:p-6">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm">
                <Settings className="mr-2 h-4 w-4" />
                Settings
              </Button>
            </div>
          </div>
          <Tabs defaultValue="new-copy" className="space-y-4">
            <TabsList>
              <TabsTrigger value="new-copy" className="flex items-center">
                <PlusCircle className="mr-2 h-4 w-4" />
                New Copy
              </TabsTrigger>
              <TabsTrigger value="history" className="flex items-center">
                <History className="mr-2 h-4 w-4" />
                History
              </TabsTrigger>
            </TabsList>
            <TabsContent value="new-copy" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Create New Copy</CardTitle>
                  <CardDescription>
                    Fill in the details about your product to generate
                    compelling marketing copy.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <CopyForm addToHistory={addToHistory} />
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="history" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Copy History</CardTitle>
                  <CardDescription>
                    View and manage your previously generated marketing copies.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <CopyHistory history={history} setHistory={setHistory} />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
      <footer className="border-t px-4 py-6 md:px-6">
        <div className="mx-auto max-w-6xl flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-gray-500 dark:text-gray-400">
            © 2025 CopyGenius. All rights reserved.
          </p>
          <nav className="flex gap-4 sm:gap-6">
            <Link
              href="#"
              className="text-xs text-gray-500 hover:underline underline-offset-4"
            >
              Terms of Service
            </Link>
            <Link
              href="#"
              className="text-xs text-gray-500 hover:underline underline-offset-4"
            >
              Privacy
            </Link>
          </nav>
        </div>
      </footer>
    </div>
  );
}
