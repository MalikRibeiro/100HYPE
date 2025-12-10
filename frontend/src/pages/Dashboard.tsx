import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getPortfolio, generateAnalysis } from '@/services/api';
import { Card, CardHeader, CardContent, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip, Legend } from 'recharts';
import ReactMarkdown from 'react-markdown';
import { Loader2, TrendingUp, DollarSign, LogOut } from 'lucide-react';
import TransactionModal from '@/components/Transactions/TransactionModal';
import { useAuth } from '@/context/AuthContext';
import { useTranslation } from 'react-i18next';
import { LanguageSelector } from '@/components/LanguageSelector';

export default function Dashboard() {
    const { logout } = useAuth();
    const { t, i18n } = useTranslation();
    const [showTxModal, setShowTxModal] = useState(false);
    const [analyzing, setAnalyzing] = useState(false);
    const [analysis, setAnalysis] = useState('');

    const { data: portfolio = [], isLoading } = useQuery({
        queryKey: ['portfolio'],
        queryFn: async () => {
            try {
                return await getPortfolio();
            } catch (e) {
                return [];
            }
        },
    });

    // Calculate KPIs
    const totalEquity = portfolio.reduce((acc: number, asset: any) => acc + (asset.total_quantity * asset.average_price), 0);
    const assetCount = portfolio.length;

    const handleAnalysis = async () => {
        setAnalyzing(true);
        try {
            // Pass the current language to the backend
            const res = await generateAnalysis(i18n.language);
            // Assuming res structure. Adjust if API returns plain text or dict
            setAnalysis(res.content || res.message || JSON.stringify(res));
        } catch (e: any) {
            console.error(e);
            const errorMsg = e.response?.data?.message || e.message || '';
            if (errorMsg.includes('429')) {
                setAnalysis(t('analysis.quotaExceeded'));
            } else {
                setAnalysis(t('analysis.error'));
            }
        } finally {
            setAnalyzing(false);
        }
    };

    // Chart Data Preparation
    const chartData = portfolio.map((a: any) => ({
        name: a.ticker,
        value: a.total_quantity * a.average_price
    })).filter((d: any) => d.value > 0);

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d', '#ffc658'];

    if (isLoading) return <div className="flex h-screen items-center justify-center"><Loader2 className="animate-spin h-8 w-8" /></div>;

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
            {/* Header */}
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">{t('dashboard.title')}</h1>
                    <p className="text-muted-foreground">{t('dashboard.overview')}</p>
                </div>
                <div className="flex gap-4 items-center">
                    <LanguageSelector />
                    <Button onClick={() => setShowTxModal(true)}>
                        <TrendingUp className="mr-2 h-4 w-4" />
                        {t('dashboard.addTransaction')}
                    </Button>
                    <Button variant="outline" onClick={logout}>
                        <LogOut className="mr-2 h-4 w-4" />
                        {t('common.logout')}
                    </Button>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">{t('dashboard.totalValue')}</CardTitle>
                        <DollarSign className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">R$ {totalEquity.toLocaleString(i18n.language, { minimumFractionDigits: 2 })}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">{t('dashboard.overview')}</CardTitle>
                        <TrendingUp className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{assetCount}</div>
                    </CardContent>
                </Card>
                {/* Add more KPIs if needed */}
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Chart Section */}
                <Card className="col-span-1">
                    <CardHeader>
                        <CardTitle>{t('dashboard.overview')}</CardTitle>
                    </CardHeader>
                    <CardContent className="h-[300px]">
                        {chartData.length > 0 ? (
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={chartData}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={60}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {chartData.map((_entry: any, index: number) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <RechartsTooltip formatter={(value: number) => `R$ ${value.toLocaleString()}`} />
                                    <Legend />
                                </PieChart>
                            </ResponsiveContainer>
                        ) : (
                            <div className="flex items-center justify-center h-full text-muted-foreground">No data available</div>
                        )}
                    </CardContent>
                </Card>

                {/* Assets Table */}
                <Card className="col-span-1 lg:col-span-2">
                    <CardHeader>
                        <CardTitle>{t('dashboard.title')}</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Ticker</TableHead>
                                    <TableHead>Category</TableHead>
                                    <TableHead className="text-right">Qty</TableHead>
                                    <TableHead className="text-right">Avg Price</TableHead>
                                    <TableHead className="text-right">{t('dashboard.totalValue')}</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {portfolio.map((asset: any) => (
                                    <TableRow key={asset.id || asset.ticker}>
                                        <TableCell className="font-medium">{asset.ticker}</TableCell>
                                        <TableCell>{asset.category}</TableCell>
                                        <TableCell className="text-right">{asset.total_quantity}</TableCell>
                                        <TableCell className="text-right">R$ {asset.average_price.toFixed(2)}</TableCell>
                                        <TableCell className="text-right font-bold">
                                            R$ {(asset.total_quantity * asset.average_price).toLocaleString(i18n.language, { minimumFractionDigits: 2 })}
                                        </TableCell>
                                    </TableRow>
                                ))}
                                {portfolio.length === 0 && (
                                    <TableRow>
                                        <TableCell colSpan={5} className="text-center">No assets found.</TableCell>
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </CardContent>
                </Card>
            </div>

            {/* AI Analysis Section */}
            <div className="mt-8">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between">
                        <CardTitle>{t('dashboard.analysisTitle')}</CardTitle>
                        <Button onClick={handleAnalysis} disabled={analyzing}>
                            {analyzing && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            {analyzing ? t('dashboard.analyzing') : t('dashboard.generateAnalysis')}
                        </Button>
                    </CardHeader>
                    <CardContent>
                        {analysis ? (
                            <div className="prose dark:prose-invert max-w-none">
                                <ReactMarkdown>{analysis}</ReactMarkdown>
                            </div>
                        ) : (
                            <div className="text-muted-foreground text-center py-8">
                                Click the button to generate an AI analysis of your portfolio.
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>

            <TransactionModal open={showTxModal} onOpenChange={setShowTxModal} />
        </div>
    );
}
