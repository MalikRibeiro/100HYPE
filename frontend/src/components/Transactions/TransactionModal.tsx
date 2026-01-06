import { useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { createAsset, createTransaction } from '@/services/api';
import { Loader2 } from 'lucide-react';
import { useQueryClient } from '@tanstack/react-query';

const schema = z.object({
    ticker: z.string().min(1, "Ticker required").transform(v => v.toUpperCase()),
    category: z.string().min(1, "Category required"),
    type: z.enum(["BUY", "SELL"]),
    date: z.string(),
    quantity: z.string().refine((v) => !isNaN(parseFloat(v)) && parseFloat(v) > 0, "Quantity must be > 0"),
    price: z.string().refine((v) => !isNaN(parseFloat(v)) && parseFloat(v) > 0, "Price must be > 0"),
});

interface TransactionModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
}

export default function TransactionModal({ open, onOpenChange }: TransactionModalProps) {
    const queryClient = useQueryClient();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const { register, handleSubmit, control, reset, formState: { errors } } = useForm({
        resolver: zodResolver(schema),
        defaultValues: {
            ticker: '',
            category: '',
            type: 'BUY' as const,
            date: new Date().toISOString().split('T')[0],
            quantity: '',
            price: ''
        }
    });

    const onSubmit = async (data: any) => {
        setLoading(true);
        setError('');
        try {
            // 1. Try create asset (if not exists)
            // Map category to API format
            const catMap: Record<string, string> = { "Ações BR": "BR_STOCKS", "FIIs": "FIIS", "Stocks": "US_STOCKS", "Cripto": "CRYPTO", "Renda Fixa": "FIXED_INCOME" };
            const apiCategory = catMap[data.category] || "OUTROS";

            let assetId = null;
            try {
                const assetRes = await createAsset({
                    ticker: data.ticker,
                    category: apiCategory,
                    name: data.ticker
                });
                assetId = assetRes.id;
            } catch (e: any) {
                // Check if it's "already exists" error, usually 400
                if (e.response && e.response.status === 400) {
                    // We don't have search API yet, so we assume backend behavior or user instruction
                    // User said: "Ativo já existe (backend precisa de ajuste para retornar ID ou buscar)."
                    // Limitation: If create fails, we might not get ID.
                    // Ideally backend CreateAsset should return existing asset if found.
                    // For now, let's assume filtering/searching is needed or backend returns ID in error?
                    // Wait, to proceed we NEED asset_id.
                    // If createAsset fails, we can't get ID easily if backend doesn't return it.
                    // Workaround: We proceed only if we got an ID. If backend returns 400, strictly speaking we are stuck unless we assume logic.
                    // Logic in Streamlit `create_transaction_flow`: "Falha... backend precisa de ajuste".
                    // But wait, the user's Streamlit code says: "Falha... Tente outro ou peça ajuste."
                    // BUT, user prompt in Step 0 says: "Ao salvar, chame a API".
                    setError("Asset creation failed. Logic gap: Backend must return ID if asset exists.");
                    // We will try.
                } else {
                    throw e;
                }
            }

            if (!assetId) {
                // Try to fetch all assets and find ID? Heavy but works.
                // Or rely on backend fix.
                // Let's assume createAsset returns the asset if it exists or we can't proceed.
                // I'll show error.
                setError("Could not retrieve Asset ID. Ensure asset is new or backend supports retrieval.");
                return;
            }

            // 2. Create Transaction
            await createTransaction({
                asset_id: assetId,
                type: data.type,
                quantity: parseFloat(data.quantity),
                price: parseFloat(data.price),
                date: data.date
            });

            queryClient.invalidateQueries({ queryKey: ['portfolio'] });
            reset();
            onOpenChange(false);
        } catch (err: any) {
            console.error(err);
            setError(err.message || "Transaction failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Add Transaction</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="ticker">Ticker</Label>
                            <Input id="ticker" placeholder="AAPL" {...register('ticker')} />
                            {errors.ticker && <p className="text-red-500 text-xs">{String(errors.ticker.message)}</p>}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="category">Category</Label>
                            <Controller
                                control={control}
                                name="category"
                                render={({ field }) => (
                                    <Select onValueChange={field.onChange} value={field.value}>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {["Ações BR", "FIIs", "Stocks", "Cripto", "Renda Fixa"].map(c => (
                                                <SelectItem key={c} value={c}>{c}</SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                )}
                            />
                            {errors.category && <p className="text-red-500 text-xs">{String(errors.category.message)}</p>}
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="type">Type</Label>
                            <Controller
                                control={control}
                                name="type"
                                render={({ field }) => (
                                    <Select onValueChange={field.onChange} value={field.value}>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Type" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="BUY">Buy</SelectItem>
                                            <SelectItem value="SELL">Sell</SelectItem>
                                        </SelectContent>
                                    </Select>
                                )}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="date">Date</Label>
                            <Input id="date" type="date" {...register('date')} />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="qty">Quantity</Label>
                            <Input id="qty" type="number" step="any" {...register('quantity')} />
                            {errors.quantity && <p className="text-red-500 text-xs">{String(errors.quantity.message)}</p>}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="price">Price (R$)</Label>
                            <Input id="price" type="number" step="0.01" {...register('price')} />
                            {errors.price && <p className="text-red-500 text-xs">{String(errors.price.message)}</p>}
                        </div>
                    </div>

                    {error && <p className="text-red-500 text-sm">{error}</p>}

                    <DialogFooter>
                        <Button type="submit" disabled={loading}>
                            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            Save Transaction
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
