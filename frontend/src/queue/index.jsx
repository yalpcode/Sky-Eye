const Queue = () => {
    let queue = [];

    const emplace = (item) => {
        queue.push(item);
    };

    const top = () => {
        if (queue.length === 0) {
            return -1;
        }
        return queue.shift();
    };

    const size = () => {
        return queue.length;
    }

    return { emplace, top, size };
};

export default Queue;
