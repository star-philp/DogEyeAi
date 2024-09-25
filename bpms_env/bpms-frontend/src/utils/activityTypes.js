// 기본 활동 유형
const defaultActivityTypes = [
    { name: 'Start', description: 'Indicates the start of a process' },
    { name: 'End', description: 'Indicates the end of a process' },
    { name: 'Task', description: 'A general task or action to be performed' },
    { name: 'Decision', description: 'A point where a decision needs to be made' },
    { name: 'Subprocess', description: 'A nested process within the main process' },
];

// 로컬 스토리지에서 사용자 정의 활동 유형 가져오기
const getUserDefinedActivityTypes = () => {
const storedTypes = localStorage.getItem('userDefinedActivityTypes');
return storedTypes ? JSON.parse(storedTypes) : [];
};

// 새로운 사용자 정의 활동 유형 추가
const addUserDefinedActivityType = (newType) => {
const userTypes = getUserDefinedActivityTypes();
userTypes.push(newType);
localStorage.setItem('userDefinedActivityTypes', JSON.stringify(userTypes));
};

// 모든 활동 유형 가져오기 (기본 + 사용자 정의)
const getAllActivityTypes = () => {
return [...defaultActivityTypes, ...getUserDefinedActivityTypes()];
};

export { 
defaultActivityTypes, 
getUserDefinedActivityTypes, 
addUserDefinedActivityType, 
getAllActivityTypes 
};