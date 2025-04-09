"use client";

import type React from "react";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2, Copy, Download, CheckCircle } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";
import { getToken } from "@/lib/auth-utils";

type CopyType = "social_media_ad" | "blog_post" | "email_campaign";

type CopyFormProps = {
  addToHistory: (entry: {
    id: string;
    productName: string;
    createdAt: string;
    preview: string;
    content: string;
  }) => void;
};

export default function CopyForm({ addToHistory }: CopyFormProps) {
  const [productName, setProductName] = useState("");
  const [productDescription, setProductDescription] = useState("");
  const [competitiveAdvantage, setCompetitiveAdvantage] = useState("");
  const [price, setPrice] = useState("");
  const [copyType, setCopyType] = useState<CopyType>("social_media_ad");
  const [image, setImage] = useState<File | null>(null);
  const [base64Image, setBase64Image] = useState<string | null>(null);
  const [imageType, setImageType] = useState<string | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedCopy, setGeneratedCopy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [isCopied, setIsCopied] = useState(false);

  const handleImageChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setImage(file);
      setImageType(file.type);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64Image = reader.result as string;
        setImagePreview(base64Image);

        // Store the base64 string in the state to use later in handleSubmit
        setBase64Image(base64Image.split(",")[1]); // Remove the "data:image/png;base64," part
        setImageType(file.type);
        // Get the image resolution (width and height)
        const img = new Image();
        img.onload = () => {
          const width = img.width;
          const height = img.height;
          // Check if image dimensions exceed 1024x1024
          if (width > 1024 || height > 1024) {
            setError(
              "Image dimensions are too large. Maximum size is 1024x1024."
            );
          } else {
            setError(null); // Clear error if image dimensions are valid
          }
        };
        img.src = base64Image;
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const accessToken = getToken();
      if (!accessToken) {
        setError("Authentication required. Please log in.");
        return;
      }
      // Create FormData object
      const formData = new FormData();
      formData.append("product_description", productDescription);
      formData.append("competitive_advantage", competitiveAdvantage);
      formData.append("price", price);

      if (image) {
        formData.append("image", base64Image ?? "");
        formData.append("image_type", imageType ?? "");
      }

      // Determine endpoint based on copy type
      const endpoint = `${process.env.NEXT_PUBLIC_API_BASE_URL}/generate_${copyType}`;

      // Make API request
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        body: formData,
      });
      if (!response.ok) {
        const errorData = await response.json();
        const errorMessage =
          errorData.detail ||
          "Request failed for an unknown reason. Please try again";
        console.error(errorMessage);
        return;
      }
      const result = await response.json();
      // Extract the generated copy based on the copy type
      let copy: string | undefined;
      if (copyType === "social_media_ad") {
        copy = result["social_media_ad"];
      } else if (copyType === "blog_post") {
        copy = result["blog_post"];
      } else if (copyType === "email_campaign") {
        copy = result["email_campaign"];
      }

      if (copy) {
        setGeneratedCopy(copy);
        setSuccessMessage("Copy generated successfully!");
        addToHistory({
          id: crypto.randomUUID(),
          productName: productDescription,
          createdAt: new Date().toISOString(),
          preview: copy.slice(0, 80) + "...",
          content: copy,
        });
        // Auto-hide success message after 3 seconds
        setTimeout(() => setSuccessMessage(null), 3000);
      } else {
        setError("Failed to generate copy. Please try again.");
      }
    } catch (error) {
      console.error("Error generating copy:", error);
      setError(
        error instanceof Error
          ? error.message
          : "An error occurred while generating copy"
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopyToClipboard = () => {
    if (generatedCopy) {
      navigator.clipboard.writeText(generatedCopy);
      setIsCopied(true);
      setSuccessMessage("Copied to clipboard!");

      // Reset the copied state after 2 seconds
      setTimeout(() => {
        setIsCopied(false);
        setSuccessMessage(null);
      }, 2000);
    }
  };

  const handleDownload = () => {
    if (generatedCopy) {
      const blob = new Blob([generatedCopy], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${productName
        .replace(/\s+/g, "-")
        .toLowerCase()}-${copyType}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setSuccessMessage("File downloaded!");
      setTimeout(() => setSuccessMessage(null), 2000);
    }
  };

  const handleReset = () => {
    setProductName("");
    setProductDescription("");
    setCompetitiveAdvantage("");
    setPrice("");
    setCopyType("social_media_ad");
    setImage(null);
    setImagePreview(null);
    setGeneratedCopy(null);
    setError(null);
    setSuccessMessage(null);
  };

  return (
    <div className="space-y-6">
      {error && (
        <Alert
          variant={
            error.includes("Copied") || error.includes("downloaded")
              ? "default"
              : "destructive"
          }
        >
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {successMessage && (
        <Alert className="bg-green-50 border-green-200 text-green-800">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription>{successMessage}</AlertDescription>
        </Alert>
      )}

      {!generatedCopy ? (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="product-name">Product Name</Label>
              <Input
                id="product-name"
                placeholder="e.g., UltraBoost Running Shoes"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="price">Price</Label>
              <Input
                id="price"
                placeholder="e.g., $99.99"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="copy-type">Copy Type</Label>
            <Select
              value={copyType}
              onValueChange={(value) => setCopyType(value as CopyType)}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select copy type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="social_media_ad">Social Media Ad</SelectItem>
                <SelectItem value="blog_post">Blog Post</SelectItem>
                <SelectItem value="email_campaign">Email Campaign</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="product-description">Product Description</Label>
            <Textarea
              id="product-description"
              placeholder="Describe your product in detail..."
              className="min-h-[100px]"
              value={productDescription}
              onChange={(e) => setProductDescription(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="competitive-advantage">Competitive Advantage</Label>
            <Textarea
              id="competitive-advantage"
              placeholder="What makes your product better than competitors?"
              className="min-h-[100px]"
              value={competitiveAdvantage}
              onChange={(e) => setCompetitiveAdvantage(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="product-image">Product Image (Optional)</Label>
            <Input
              id="product-image"
              type="file"
              accept="image/*"
              onChange={handleImageChange}
            />
            {imagePreview && (
              <div className="mt-2">
                <img
                  src={imagePreview || "/placeholder.svg"}
                  alt="Product preview"
                  className="max-h-40 rounded-md object-contain"
                />
              </div>
            )}
          </div>
          <div className="flex justify-end gap-2">
            <Button type="button" variant="outline" onClick={handleReset}>
              Reset
            </Button>
            <Button type="submit" disabled={isGenerating || error !== null}>
              {isGenerating ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating...
                </>
              ) : (
                "Generate Copy"
              )}
            </Button>
          </div>
        </form>
      ) : (
        <div className="space-y-4">
          <div className="flex justify-between">
            <h3 className="text-lg font-medium">Generated Copy</h3>
            <div className="flex gap-2">
              <Button
                size="sm"
                variant="outline"
                onClick={handleCopyToClipboard}
              >
                {isCopied ? (
                  <CheckCircle className="mr-2 h-4 w-4" />
                ) : (
                  <Copy className="mr-2 h-4 w-4" />
                )}
                {isCopied ? "Copied" : "Copy"}
              </Button>
              <Button size="sm" variant="outline" onClick={handleDownload}>
                <Download className="mr-2 h-4 w-4" />
                Download
              </Button>
              <Button size="sm" variant="outline" onClick={handleReset}>
                Create New
              </Button>
            </div>
          </div>

          <Tabs defaultValue="preview">
            <TabsList>
              <TabsTrigger value="preview">Preview</TabsTrigger>
              <TabsTrigger value="markdown">Markdown</TabsTrigger>
            </TabsList>
            <TabsContent value="preview" className="mt-4">
              <Card>
                <CardContent className="p-4">
                  <div className="prose max-w-none dark:prose-invert">
                    {generatedCopy.split("\n\n").map((paragraph, index) => {
                      if (paragraph.startsWith("# ")) {
                        return (
                          <h1 key={index} className="text-2xl font-bold mt-0">
                            {paragraph.substring(2)}
                          </h1>
                        );
                      } else if (paragraph.startsWith("## ")) {
                        return (
                          <h2
                            key={index}
                            className="text-xl font-semibold mt-4"
                          >
                            {paragraph.substring(3)}
                          </h2>
                        );
                      } else {
                        return (
                          <p key={index} className="my-2">
                            {paragraph}
                          </p>
                        );
                      }
                    })}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="markdown" className="mt-4">
              <Card>
                <CardContent className="p-4">
                  <pre className="bg-muted p-4 rounded-md overflow-auto whitespace-pre-wrap">
                    {generatedCopy}
                  </pre>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      )}
    </div>
  );
}
