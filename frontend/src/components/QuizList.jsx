import apiInstance from "@/utils/axios";
import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { useNavigate } from "react-router-dom";


const QuizList = () => {
    const [quizzes, setQuizzes] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        getQuizzes();
    }, []);

    const getQuizzes = async () => {
        try {
            const response = await apiInstance.get('/quiz/');
            setQuizzes(response.data.filter(quiz => quiz.is_active));
            console.log(response.data);
        } catch (error) {
            console.error(error);
        }
    }

    const startQuiz = (id) => {
        console.log(id);
        navigate(`/quiz/${id}`);
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-6">Available Quizzes</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {quizzes && quizzes.map((quiz) => (
                    <Card key={quiz.id} className="p-4 rounded-md hover:shadow-lg transition-shadow">
                        <CardHeader>
                            <CardTitle className="text-lg font-semibold mb-2">{quiz.title}</CardTitle>
                            <CardDescription className="text-sm text-gray-500">{quiz.description}</CardDescription>     
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-2">
                                <p>Time Limit: {quiz.time_limit} minutes</p>
                                <Button
                                    onClick={() => startQuiz(quiz.id)}
                                >
                                    Start Quiz
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    )
}

export default QuizList