"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Eye, Copy, Trash2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

type CopyItem = {
  id: string;
  productName: string;
  createdAt: string;
  preview: string;
  content: string;
};

type CopyHistoryProps = {
  history: CopyItem[];
  setHistory: React.Dispatch<React.SetStateAction<CopyItem[]>>;
};

export default function CopyHistory({ history, setHistory }: CopyHistoryProps) {
  const [selectedCopy, setSelectedCopy] = useState<CopyItem | null>(null);

  const formatDate = (dateString: string) =>
    new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  const handleDelete = (id: string) => {
    setHistory((prev) => prev.filter((item) => item.id !== id));
  };

  const handleCopyToClipboard = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  return (
    <div className="space-y-4">
      {history.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-muted-foreground">No copy history found</p>
        </div>
      ) : (
        history.map((item) => (
          <Card key={item.id}>
            <CardContent className="p-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <h3 className="font-medium">{item.productName}</h3>
                  <p className="text-sm text-muted-foreground">
                    Created {formatDate(item.createdAt)}
                  </p>
                </div>
                <div className="flex items-center gap-2 self-end sm:self-auto">
                  <Dialog>
                    <DialogTrigger asChild>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setSelectedCopy(item)}
                      >
                        <Eye className="h-4 w-4 mr-1" />
                        View
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="max-w-2xl">
                      <DialogHeader>
                        <DialogTitle>{selectedCopy?.productName}</DialogTitle>
                        <DialogDescription>
                          Created{" "}
                          {selectedCopy && formatDate(selectedCopy.createdAt)}
                        </DialogDescription>
                      </DialogHeader>
                      <div className="mt-4 max-h-[60vh] overflow-y-auto">
                        <div className="prose max-w-none dark:prose-invert">
                          {selectedCopy?.content
                            .split("\n\n")
                            .map((paragraph, i) =>
                              paragraph.startsWith("# ") ? (
                                <h1 key={i} className="text-2xl font-bold mt-0">
                                  {paragraph.slice(2)}
                                </h1>
                              ) : paragraph.startsWith("## ") ? (
                                <h2
                                  key={i}
                                  className="text-xl font-semibold mt-4"
                                >
                                  {paragraph.slice(3)}
                                </h2>
                              ) : (
                                <p key={i} className="my-2">
                                  {paragraph}
                                </p>
                              )
                            )}
                        </div>
                      </div>
                      <div className="flex justify-end gap-2 mt-4">
                        <Button
                          variant="outline"
                          onClick={() =>
                            handleCopyToClipboard(selectedCopy?.content || "")
                          }
                        >
                          <Copy className="h-4 w-4 mr-2" />
                          Copy
                        </Button>
                      </div>
                    </DialogContent>
                  </Dialog>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleCopyToClipboard(item.content)}
                  >
                    <Copy className="h-4 w-4 mr-1" />
                    Copy
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleDelete(item.id)}
                  >
                    <Trash2 className="h-4 w-4 mr-1" />
                    Delete
                  </Button>
                </div>
              </div>
              <p className="text-sm mt-2 line-clamp-2">{item.preview}</p>
            </CardContent>
          </Card>
        ))
      )}
    </div>
  );
}
