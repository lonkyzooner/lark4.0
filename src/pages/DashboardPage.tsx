import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useStripe } from '../contexts/StripeContext';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { CheckCircle2, ArrowRight, Shield } from 'lucide-react';
import App from '../App';

const DashboardPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { subscriptionTier } = useStripe();
  const [showSuccess, setShowSuccess] = useState(false);
  
  useEffect(() => {
    // Check if we're coming from a successful subscription
    const urlParams = new URLSearchParams(location.search);
    const isSuccess = urlParams.get('subscription') === 'success';
    
    if (isSuccess) {
      setShowSuccess(true);
      
      // Remove the query parameter after a delay
      const timer = setTimeout(() => {
        navigate('/dashboard', { replace: true });
      }, 5000);
      
      return () => clearTimeout(timer);
    }
  }, [location, navigate]);
  
  // Determine subscription level for display
  const subscriptionName = subscriptionTier === 'premium' 
    ? 'Premium' 
    : subscriptionTier === 'standard'
      ? 'Standard'
      : subscriptionTier === 'enterprise'
        ? 'Enterprise'
        : 'Basic';
  
  // If showing success message, render that first
  if (showSuccess) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-900 to-blue-950 flex items-center justify-center p-4">
        <Card className="w-full max-w-md border-2 border-green-500 bg-blue-950/50">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 bg-green-500/20 p-3 rounded-full w-16 h-16 flex items-center justify-center">
              <CheckCircle2 className="h-10 w-10 text-green-500" />
            </div>
            <CardTitle className="text-2xl text-white">Subscription Activated!</CardTitle>
            <CardDescription className="text-blue-200">
              Your {subscriptionName} plan is now active
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center text-blue-100">
            <p>Thank you for subscribing to LARK. You now have access to all {subscriptionName} features.</p>
          </CardContent>
          <CardFooter className="flex justify-center">
            <Button 
              onClick={() => setShowSuccess(false)}
              className="bg-blue-600 hover:bg-blue-500"
            >
              Continue to Dashboard <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </CardFooter>
        </Card>
      </div>
    );
  }
  
  // Otherwise show the main dashboard with the App component
  return (
    <div className="min-h-screen">
      <div className="bg-gradient-to-r from-blue-900 to-blue-800 p-4 shadow-md">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">LARK Dashboard</h1>
            <p className="text-blue-200">
              {subscriptionTier ? `${subscriptionName} Plan` : 'Welcome to LARK'}
            </p>
          </div>
          <div className="flex items-center gap-2">
            {subscriptionTier && (
              <div className="bg-blue-800/50 px-3 py-1 rounded-full flex items-center text-sm text-blue-100">
                <Shield className="h-4 w-4 mr-1 text-blue-300" />
                {subscriptionName}
              </div>
            )}
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => navigate('/account')}
              className="text-white border-blue-400 hover:bg-blue-800"
            >
              Account
            </Button>
          </div>
        </div>
      </div>
      
      <App />
    </div>
  );
};

export default DashboardPage;
