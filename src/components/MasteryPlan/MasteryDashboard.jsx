/**
 * MasteryDashboard Component
 * 
 * @author EULOGE MABIALA
 * @description Dashboard principal pour la gestion des plans de maîtrise
 * @version 2.0.0
 */

import React, { useState, useEffect } from 'react';
import { 
  Upload, 
  BookOpen, 
  Target, 
  CheckCircle, 
  Clock, 
  TrendingUp, 
  Sparkles,
  Brain,
  Zap,
  Award,
  Calendar,
  Users,
  BarChart3,
  Plus
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import DocumentUploader from './DocumentUploader';
import PlanGenerator from './PlanGenerator';
import ValidationChecklist from './ValidationChecklist';

const MasteryDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [analyzedDocs, setAnalyzedDocs] = useState([]);

  useEffect(() => {
    fetchSubjects();
  }, []);

  const fetchSubjects = async () => {
    try {
      const response = await fetch('/api/mastery/get-subjects');
      const data = await response.json();
      if (data.status === 'success') {
        setSubjects(data.subjects);
      } else if (Array.isArray(data)) {
        // compatibilité ancienne forme
        setSubjects(data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des matières:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadComplete = (docs) => {
    setAnalyzedDocs(docs || []);
    // recharger les sujets si nécessaire
    fetchSubjects();
    // basculer vers le générateur pour utiliser les docs analysés
    setActiveTab('generator');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'from-green-500 to-emerald-500';
      case 'in-progress': return 'from-blue-500 to-cyan-500';
      case 'not-started': return 'from-gray-400 to-gray-500';
      default: return 'from-gray-400 to-gray-500';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed': return 'Maîtrisé';
      case 'in-progress': return 'En cours';
      case 'not-started': return 'À commencer';
      default: return 'Inconnu';
    }
  };

  const renderOverview = () => (
    <div className="space-y-8">
      {/* Hero + stats... (inchangé) */}
    </div>
  );

  return (
    <div className="space-y-6">
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4 bg-white/70 backdrop-blur-lg border-0 shadow-lg rounded-xl p-1">
          <TabsTrigger value="overview"> <BookOpen className="h-4 w-4 mr-2"/>Vue d'ensemble</TabsTrigger>
          <TabsTrigger value="upload"> <Upload className="h-4 w-4 mr-2"/>Upload</TabsTrigger>
          <TabsTrigger value="generator"> <Target className="h-4 w-4 mr-2"/>Générateur</TabsTrigger>
          <TabsTrigger value="validation"> <CheckCircle className="h-4 w-4 mr-2"/>Validation</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-6">
          {renderOverview()}
        </TabsContent>

        <TabsContent value="upload" className="mt-6">
          <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-6 text-white mb-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
                <Upload className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">Upload de Contenu</h2>
                <p className="text-green-100">Transformez vos documents en plans de maîtrise intelligents</p>
              </div>
            </div>
          </div>
          <DocumentUploader onUploadComplete={handleUploadComplete} />
        </TabsContent>

        <TabsContent value="generator" className="mt-6">
          <div className="bg-gradient-to-r from-purple-500 to-pink-600 rounded-2xl p-6 text-white mb-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
                <Target className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">Générateur de Plans</h2>
                <p className="text-purple-100">Créez des parcours d'apprentissage personnalisés avec l'IA</p>
              </div>
            </div>
          </div>
          <PlanGenerator analyzedDocuments={analyzedDocs} onPlanGenerated={fetchSubjects} />
        </TabsContent>

        <TabsContent value="validation" className="mt-6">
          <div className="bg-gradient-to-r from-orange-500 to-red-600 rounded-2xl p-6 text-white mb-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
                <CheckCircle className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">Validation de Maîtrise</h2>
                <p className="text-orange-100">Certifiez votre apprentissage en 5 étapes de validation</p>
              </div>
            </div>
          </div>
          <ValidationChecklist subjects={subjects} onValidationComplete={fetchSubjects} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MasteryDashboard;