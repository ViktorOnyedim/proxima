// import { useEffect, useState } from "react"
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card";
// import { Button } from '@/components/ui/button';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import apiInstance from "@/utils/axios";
// import { Checkbox } from '@/components/ui/checkbox';
// import { Input } from '@/components/ui/input';
// import { Alert, AlertDescription } from '@/components/ui/alert'
// import axios from "axios";
import { useEffect, useState } from "react";

const QuizApp = () => {
    const [quiz, setQuiz] = useState([]);
    // const [currentQuestion, setCurrentQuestion] = useState(0);
    const [question, setQuestion] = useState([])
    // const [timeLeft, setTimeLeft] = useState({});


    const getQuiz = async () => {
        try {
            const response = await apiInstance.get('/quiz/1/');
            setQuiz(response.data);
            console.log(response.data)
        } catch (error) {
            console.error(error);
        }
    }

    useEffect(() => {
        getQuiz();
    }, []);

    useEffect(() => {
        const getQuestion = async () => {
            try {
                const response = await apiInstance.get('/questions/1/');
                setQuestion(response.data);
                // console.log(response.data);
            } catch (error) {
                console.error(error)
            }
        };
        getQuestion();

    }, []);

    return (
        <Card className="max-w-2xl mx-auto my-8">
            <CardHeader>
                <CardTitle>{quiz.title}</CardTitle>
                <div className="text-sm text-gray-500">
                    Time remaining (Limit): {quiz.time_limit}
                </div>
            </CardHeader>
            <CardContent>
                <div className="space-y-6">
                    <div className="text-lg font-medium">
                        Question {question.order}
                    </div>
                
                    <div className="text-base">{question.text}</div>
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
                </div>   
            </CardContent>
    </Card>
  );
};

export default QuizApp