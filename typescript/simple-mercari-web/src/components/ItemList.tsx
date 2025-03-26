import { useEffect, useState } from 'react';
import { Item, fetchItems } from '~/api';

const PLACEHOLDER_IMAGE = import.meta.env.VITE_FRONTEND_URL + '/logo192.png';
const getImageUrl = (imageName: string) => `http://localhost:9000/image/${imageName}`;

interface Prop {
  reload: boolean;
  onLoadCompleted: () => void;
}

export const ItemList = ({ reload, onLoadCompleted }: Prop) => {
  const [items, setItems] = useState<Item[]>([]);
  useEffect(() => {
    const fetchData = () => {
      fetchItems()
        .then((data) => {
          console.debug('GET success:', data);
          setItems(data.items);
          onLoadCompleted();
        })
        .catch((error) => {
          console.error('GET error:', error);
        });
    };

    if (reload) {
      fetchData();
    }
  }, [reload, onLoadCompleted]);

  return (
    <div className="ItemList">
      <div className="item-grid">
      {items?.map((item) => (
        // return (
          <div key={item.id}>
            {/* TODO: Task 2: Show item images */}
            <div className="image-container">
              <img src={getImageUrl(item.image_name)} alt={item.name} onError={(e) => (e.currentTarget.src = PLACEHOLDER_IMAGE)}/>
            </div>
            {/* <img
              // src={PLACEHOLDER_IMAGE}
              src={getImageUrl(item.image_name)}
              alt={item.name}
              onError={(e) => (e.currentTarget.src = PLACEHOLDER_IMAGE)}
            /> */}
            <p>
              <span>Name: {item.name}</span>
              <br />
              <span>Category: {item.category}</span>
            </p>
          </div>
        // );
      ))}
      </div>
    </div>
  );
};
