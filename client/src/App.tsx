import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import AdminUsers from "./pages/AdminUsers";
import AdminQuizzes from "./pages/AdminQuizzes";
import QuizDashboard from "./pages/QuizDashboard";
import ModeratorQuizzes from "./pages/ModeratorQuizzes";
import CreateQuiz from "./pages/CreateQuiz";
import AvailableQuizzes from "./pages/AvailableQuizzes";
import PlayQuiz from "./pages/PlayQuiz";
import QuizLeaderboard from "./pages/QuizLeaderboard";
import QuizResults from "./pages/QuizResults";
import SelectQuizForLeaderboard from "./pages/SelectQuizForLeaderboard";


function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />

          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />

            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />

            <Route
              path="/admin/users"
              element={
                <ProtectedRoute allowedRoles={["ADMINISTRATOR"]}>
                  <AdminUsers />
                </ProtectedRoute>
              }
            />

            <Route
              path="/kvizovi/admin"
              element={
                <ProtectedRoute allowedRoles={["ADMINISTRATOR"]}>
                  <AdminQuizzes />
                </ProtectedRoute>
              }
            />

            <Route
              path="/kvizovi"
              element={
                <ProtectedRoute>
                  <QuizDashboard />
                </ProtectedRoute>
              }
            />

            <Route
              path="/kvizovi/moji"
              element={
                <ProtectedRoute allowedRoles={["MODERATOR"]}>
                  <ModeratorQuizzes />
                </ProtectedRoute>
              }
            />

            <Route
              path="/kvizovi/kreiraj"
              element={
                <ProtectedRoute allowedRoles={["MODERATOR"]}>
                  <CreateQuiz />
                </ProtectedRoute>
              }
            />

            <Route
              path="/kvizovi/dostupni"
              element={
                <ProtectedRoute allowedRoles={["IGRAC"]}>
                  <AvailableQuizzes />
                </ProtectedRoute>
              }
            />

            <Route
              path="/kvizovi/:id/play"
              element={
                <ProtectedRoute allowedRoles={["IGRAC"]}>
                  <PlayQuiz />
                </ProtectedRoute>
              }
            />

            <Route
              path="/kvizovi/rezultati"
              element={
                <ProtectedRoute allowedRoles={["IGRAC"]}>
                  <QuizResults />
                </ProtectedRoute>
              }
            />

            <Route
              path="/kvizovi/rang-liste"
              element={
                <ProtectedRoute allowedRoles={["ADMINISTRATOR", "MODERATOR"]}>
                  <SelectQuizForLeaderboard />
                </ProtectedRoute>
              }
            />

            <Route
              path="/kvizovi/:id/leaderboard"
              element={
                <ProtectedRoute allowedRoles={["ADMINISTRATOR", "MODERATOR"]}>
                  <QuizLeaderboard />
                </ProtectedRoute>
              }
            />


            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
