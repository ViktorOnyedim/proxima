import { useEffect, useState } from "react"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card";
import { Button } from '@/components/ui/button';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import apiInstance from "@/utils/axios";
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { Timer } from 'lucide-react';

const QuizApp = () => {
    const [quiz, setQuiz] = useState([]);
    const [timeLeft, setTimeLeft] = useState(null);

    const getQuiz = async () => {
        try {
            const response = await apiInstance.get('/quiz/1/');
            setQuiz(response.data);
            console.log(response.data)

            // Set up timer
            const [hours, mins, secs] = response.data.time_limit.split(":").map(Number);
            const totalSeconds = hours * 3600 + mins * 60 + secs;
            setTimeLeft(totalSeconds);
        } catch (error) {
            console.error(error);
        }
    }

    useEffect(() => {
        getQuiz();
    }, []);

    useEffect(() => {
        if (timeLeft === null || timeLeft <= 0) return;
        const timer = setInterval(() => {
            setTimeLeft(prev => {
                if (prev <= 1) {
                    clearInterval(timer);
                    // handleSubmit();
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);

        return () => clearInterval(timer);
    }, [timeLeft]);

    const formatTime = (seconds) => {
        const hours = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return [hours, mins, secs % 60]
            .map(unit => unit.toString().padStart(2, '0'))
            .join(':');
    };

    return (
        <Card className="max-w-2xl mx-auto my-8">
            <CardHeader>
                <CardTitle>{quiz.title}</CardTitle>
                <CardDescription>{quiz.description}</CardDescription>
                <div className="text-sm text-gray-500">
                    Time remaining (Limit): {quiz.time_limit}
                </div>
                <div className="flex items-center gap-2 text-lg font-semibold">
                    <Timer className="w-5 h-5" />
                    {formatTime(timeLeft)}
                </div>
            </CardHeader>
            <CardContent>
                <div className="space-y-6">
                    {quiz.questions && quiz.questions.map((question) => (
                        <div key={question.id} className="space-y-4">
                            <h3 className="font-medium">
                                {question.order}. {question.text}
                            </h3>

                            {(question.type === "SC" || question.type === "B") && (
                            <RadioGroup>
                                {question.choices.map((choice) => (
                                    <div key={choice.id} className="flex items-center space-x-2">
                                        <RadioGroupItem value={choice.id} id={`choice-${choice.id}`} />
                                    <label htmlFor={`choice-${choice.id}`}>{choice.text}</label>
                                </div>
                                ))}
                            </RadioGroup>
                            )}

                            {question.type === "MC" && (
                                <div className="space-y-2">
                                    {question.choices.map((choice) => (
                                        <div key={choice.id} className="flex items-center space-x-2">
                                            <Checkbox id={`choice-${choice.id}`} />
                                            <label htmlFor={`choice-${choice.id}`}>{choice.text}</label>
                                        </div> 
                                    ))}
                                </div>
                            )}

                            {question.type === "T" && (
                                <Input placeholder="Type your answer here" />
                            )}
                        </div>
                    ))}                   
                </div>
                <Button className="mt-6 w-full">Submit Quiz</Button>
            </CardContent>
    </Card>
  );
};

export default QuizApp